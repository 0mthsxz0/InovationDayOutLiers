from contextlib import closing
from json import dumps, loads
from os import getenv
import sqlite3

from datetime import date
from typing import Any, Dict, List

FONTE = "Capturas do Innovation Day IBMEC, calendário 2026.2"


def evento(nome, inicio, fim, tipo, publico, precisao="dia", fonte=FONTE):
    return dict(nome=nome, inicio=date.fromisoformat(inicio), fim=date.fromisoformat(fim),
                tipo=tipo, publico=publico, precisao=precisao, fonte=fonte)


FONTE_2026_1 = "Imagem do Calendário Acadêmico IBMEC 2026.1 (campus e versão não identificados)"

EVENTOS = {
    "2026.1": [
        evento("Abertura da renovação e alteração de disciplinas", "2026-01-20", "2026-01-20",
               "matricula", "Alunos", fonte=FONTE_2026_1),
        evento("Início das aulas de veteranos", "2026-02-09", "2026-02-09",
               "acolhimento", "Veteranos", fonte=FONTE_2026_1),
        evento("Início das aulas de calouros", "2026-02-23", "2026-02-23",
               "acolhimento", "Calouros", fonte=FONTE_2026_1),
        evento("Aplicação da AP1", "2026-04-13", "2026-04-17",
               "avaliacao", "Alunos e docentes", fonte=FONTE_2026_1),
        evento("Fechamento da AP1", "2026-04-30", "2026-04-30",
               "notas", "Docentes e Secretaria", fonte=FONTE_2026_1),
        evento("Aplicação da AP2", "2026-06-11", "2026-06-17",
               "avaliacao", "Alunos e docentes", fonte=FONTE_2026_1),
        evento("Aplicação das avaliações substitutivas", "2026-06-23", "2026-06-30",
               "avaliacao", "Alunos e docentes", fonte=FONTE_2026_1),
        evento("Fechamento dos diários de frequência", "2026-07-01", "2026-07-01",
               "diarios", "Docentes e Secretaria", fonte=FONTE_2026_1),
    ],
    "2026.2": [
        evento("Matrícula e rematrícula", "2026-07-01", "2026-07-31", "matricula", "Alunos", "mes"),
        evento("Início das aulas de veteranos", "2026-08-03", "2026-08-03", "acolhimento", "Veteranos"),
        evento("Início das aulas de calouros", "2026-08-10", "2026-08-10", "acolhimento", "Calouros"),
        evento("Prazo final para trancamento", "2026-10-09", "2026-10-09", "matricula", "Alunos"),
        evento("Fechamento da AP1", "2026-10-13", "2026-10-13", "notas", "Docentes e Secretaria"),
        evento("Aplicação da AP2", "2026-11-12", "2026-11-18", "avaliacao", "Alunos e docentes"),
        evento("Prazo final de notas da AC", "2026-11-16", "2026-11-16", "notas", "Docentes e Secretaria"),
        evento("Lançamento de notas da AP2", "2026-11-23", "2026-11-23", "notas", "Docentes e Secretaria"),
        evento("Bancas de TCC e monografia", "2026-11-23", "2026-11-28", "bancas", "Alunos e docentes"),
        evento("Avaliações substitutivas", "2026-11-25", "2026-12-03", "avaliacao", "Alunos e docentes"),
        evento("Vestibular 2027.1", "2026-11-27", "2026-11-28", "vestibular", "Candidatos"),
    ],
}

TABELA_SIA_CALENDARIO: List[Dict[str, Any]] = [
    {
        "semestre": "2026.1",
        "dt_evento": data,
        "tipo_evento": tipo,
        "descricao_evento": descricao
    }
    for data, tipo, descricao in [
        (date(2026, 2, 16), "RECESSO", "Carnaval"),
        (date(2026, 2, 17), "RECESSO", "Carnaval"),
        (date(2026, 2, 18), "RECESSO", "Carnaval"),
        (date(2026, 4, 2), "RECESSO", "Semana Santa"),
        (date(2026, 4, 3), "RECESSO", "Semana Santa"),
        (date(2026, 4, 20), "RECESSO", "Tiradentes"),
        (date(2026, 4, 21), "FERIADO", "Tiradentes"),
        (date(2026, 5, 1), "FERIADO", "Dia do Trabalho"),
        (date(2026, 6, 4), "FERIADO", "Corpus Christi"),
        (date(2026, 6, 5), "RECESSO", "Corpus Christi"),
    ]
]

def _calendario_inicial(semestre: str = "2026.1") -> Dict[str, Any]:
    eventos = [e for e in TABELA_SIA_CALENDARIO if e["semestre"] == semestre]
    calendario = {
        "semestre_referencia": semestre,
        "feriados_e_recessos": [
            {"data": e["dt_evento"], "descricao": e["descricao_evento"]}
            for e in eventos
        ]
    }
    if semestre in EVENTOS:
        calendario["eventos_academicos"] = EVENTOS[semestre]
    return calendario

def montar_json_calendario(semestre: str = "2026.1") -> Dict[str, Any]:
    caminho = getenv("IBMEC_CALENDARIO_DB", "calendario_academico.sqlite3")
    with closing(sqlite3.connect(caminho, timeout=5)) as banco, banco:
        banco.execute("""
            CREATE TABLE IF NOT EXISTS calendario (
                semestre TEXT PRIMARY KEY,
                conteudo TEXT NOT NULL
            )
        """)
        linha = banco.execute(
            "SELECT conteudo FROM calendario WHERE semestre = ?", (semestre,)
        ).fetchone()
        if linha is None and semestre in EVENTOS:
            banco.execute(
                "INSERT OR IGNORE INTO calendario VALUES (?, ?)",
                (semestre, dumps(_calendario_inicial(semestre), default=str, ensure_ascii=False)),
            )
            linha = banco.execute(
                "SELECT conteudo FROM calendario WHERE semestre = ?", (semestre,)
            ).fetchone()
    if linha is None:
        return {"semestre_referencia": semestre, "feriados_e_recessos": []}
    return loads(linha[0])
