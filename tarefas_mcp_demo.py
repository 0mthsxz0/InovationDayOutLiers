import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from math import floor
from pathlib import Path
from zoneinfo import ZoneInfo

from calendario_academico import EVENTOS, TABELA_SIA_CALENDARIO
from dados_mcp_demo import ALUNOS, PERFIS
from plano_operacional import montar_plano

REGRAS = {
    "aluno": {
        "boletos": "Vencimento de boleto em D−7, D−2 e D−1",
        "faltas": "Verificação semanal de risco por faltas",
    },
    "professor": {
        "provas": "Início das avaliações em D−7",
        "notas": "Prazo de lançamento de notas em D−7",
    },
    "ti": {"picos": "Janelas de risco operacional em D−7"},
    "suporte": {"grades": "Revisão de grades em D−7 do início das aulas"},
}

DIAS_SEMANA = (
    "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
    "Sexta-feira", "Sábado", "Domingo",
)


def hoje_local() -> date:
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date()


def alertas_aluno(identidade, ativacao, hoje):
    dados = ALUNOS[identidade]
    for vencimento in dados["boletos"]:
        for dias in (7, 2, 1):
            aviso = vencimento - timedelta(days=dias)
            if ativacao <= aviso <= hoje <= vencimento:
                yield "boletos", aviso, f"Boleto fictício com vencimento em {vencimento:%d/%m/%Y}. Aviso D−{dias}."

    semestre = dados["notas"]["semestre_atual"]
    inicio = next((e["inicio"] for e in EVENTOS.get(semestre, [])
                   if e["nome"] == "Início das aulas de veteranos"), None)
    # A base de demonstração só contém grades e faltas para 2026.1.
    fim = date(2026, 7, 3)
    if inicio is None or not max(inicio, ativacao) <= hoje <= fim:
        return
    semana = hoje - timedelta(days=hoje.weekday())
    if semana < ativacao:
        return
    dias_sem_aula = {e["dt_evento"] for e in TABELA_SIA_CALENDARIO if e["semestre"] == semestre}
    grades = {d["codigo_disciplina"]: d["aulas"] for d in dados["grade"]["grade"]}
    for disciplina in dados["notas"]["disciplinas"]:
        dias = [DIAS_SEMANA.index(a["dia_da_semana"])
                for a in grades.get(disciplina["codigo_disciplina"], [])]
        aulas = sum(dia == (inicio + timedelta(days=i)).weekday()
                    for i in range((fim - inicio).days + 1)
                    if inicio + timedelta(days=i) not in dias_sem_aula
                    for dia in dias)
        faltas = disciplina["frequencia"]["faltas_acumuladas"]
        if aulas and (100 * faltas / aulas >= 19 or floor(aulas * 0.25) - faltas <= 2):
            yield "faltas", semana, f"{disciplina['nome_disciplina']}: {faltas} faltas registradas em {aulas} aulas úteis previstas."


def alertas_calendario(papel, ativacao, hoje):
    for semestre, eventos in EVENTOS.items():
        if papel == "ti":
            plano = montar_plano(semestre)
            acoes = {acao["evento"]: acao for acao in plano["acoes"]}
            for e in eventos:
                aviso = e["inicio"] - timedelta(days=7)
                if e["precisao"] == "dia" and ativacao <= aviso <= hoje <= e["fim"]:
                    acao = acoes[e["nome"]]
                    yield "picos", aviso, (
                        f"Risco operacional em {e['nome']} ({e['inicio']:%d/%m} a {e['fim']:%d/%m/%Y}). "
                        f"Serviço: {acao['servico']}. {acao['acao']}"
                    )
            for janela in plano["sobreposicoes"]:
                aviso = janela["inicio"] - timedelta(days=7)
                if ativacao <= aviso <= hoje <= janela["fim"]:
                    simultaneos = ", ".join(janela["eventos"])
                    yield "picos", aviso, (
                        f"Risco operacional de {janela['inicio']:%d/%m} a {janela['fim']:%d/%m/%Y}. "
                        f"Eventos simultâneos: {simultaneos}."
                    )
            continue
        tipos = {"avaliacao": "provas", "notas": "notas"} if papel == "professor" else {"acolhimento": "grades"}
        for e in eventos:
            regra = tipos.get(e["tipo"])
            aviso = e["inicio"] - timedelta(days=7)
            if regra and e["precisao"] == "dia" and ativacao <= aviso <= hoje <= e["fim"]:
                mensagem = f"{e['nome']} em {e['inicio']:%d/%m/%Y}."
                if e["fim"] != e["inicio"]:
                    mensagem = f"{e['nome']} de {e['inicio']:%d/%m} a {e['fim']:%d/%m/%Y}."
                if papel == "suporte":
                    mensagem += " Revise as grades para preparar o atendimento."
                yield regra, aviso, mensagem


class TarefasDemo:
    def __init__(self, caminho: str):
        self.caminho = Path(caminho)

    def conectar(self):
        return closing(sqlite3.connect(self.caminho, timeout=5))

    def preparar(self):
        with self.conectar() as banco, banco:
            banco.executescript("""
                CREATE TABLE IF NOT EXISTS ativacoes (
                    conta TEXT PRIMARY KEY, data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS avisos (
                    conta TEXT NOT NULL, regra TEXT NOT NULL, data TEXT NOT NULL,
                    mensagem TEXT NOT NULL, PRIMARY KEY (conta, regra, data, mensagem)
                );
            """)

    def ativar(self, identidade, hoje):
        with self.conectar() as banco, banco:
            banco.execute("INSERT OR IGNORE INTO ativacoes VALUES (?, ?)", (identidade, hoje.isoformat()))

    def processar(self, hoje):
        with self.conectar() as banco, banco:
            for identidade, data in banco.execute("SELECT conta, data FROM ativacoes").fetchall():
                papel = PERFIS[identidade]
                ativacao = date.fromisoformat(data)
                ocorrencias = (
                    alertas_aluno(identidade, ativacao, hoje) if papel == "aluno"
                    else alertas_calendario(papel, ativacao, hoje)
                )
                banco.executemany(
                    "INSERT OR IGNORE INTO avisos VALUES (?, ?, ?, ?)",
                    ((identidade, regra, dia.isoformat(), mensagem)
                     for regra, dia, mensagem in ocorrencias),
                )

    def listar(self, identidade, hoje):
        self.processar(hoje)
        with self.conectar() as banco:
            ativacao = banco.execute("SELECT data FROM ativacoes WHERE conta = ?", (identidade,)).fetchone()
            avisos = banco.execute(
                "SELECT regra, data, mensagem FROM avisos WHERE conta = ? ORDER BY data DESC LIMIT 20",
                (identidade,),
            ).fetchall()
        papel = PERFIS[identidade]
        return {
            "perfil": papel,
            "ativado_em": ativacao[0] if ativacao else None,
            "tarefas": list(REGRAS[papel].values()) if ativacao else [],
            "avisos": [{"regra": regra, "data": dia, "mensagem": mensagem}
                       for regra, dia, mensagem in avisos],
        }
