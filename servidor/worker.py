from datetime import date, timedelta
import math
import sia_database as sia

MAPA_DIAS = {
    "Segunda-feira": 0,
    "Terça-feira": 1,
    "Quarta-feira": 2,
    "Quinta-feira": 3,
    "Sexta-feira": 4,
    "Sábado": 5,
    "Domingo": 6
}

def executar_job_financeiro(data_referencia: date):
    print(f"\n[JOB FINANCEIRO] Avaliando boletos em aberto para a data {data_referencia}...")
    for t in sia.TABELA_SIA_TITULOS:
        if t["cod_status"] == "PENDENTE":
            dias_restantes = (t["dt_vencimento"] - data_referencia).days
            if dias_restantes in [7, 2, 1]:
                print("=" * 60)
                print(f"ALERTA PROATIVO FINANCEIRO: Matrícula {t['matricula_aluno']}")
                print(f"Vencimento em {dias_restantes} dia(s) ({t['dt_vencimento']}). Valor: R$ {t['vlr_nominal']:.2f}")
                print(f"Linha Digitável: {t['linha_digitavel']}")
                print(f"PIX: {t['url_pix']}")
                print("=" * 60)

def executar_job_academico_faltas():
    print("\n[JOB ACADÊMICO] Projetando calendário letivo e calculando tetos de faltas...")

    for aluno in sia.TABELA_SIA_ALUNOS:
        matricula = aluno["matricula"]
        limite_pref = aluno["cfg_limite_alerta_freq"]

        inscricoes = [m for m in sia.TABELA_SIA_MATRICULAS_DISCIPLINAS if m["matricula_aluno"] == matricula]
        for inscricao in inscricoes:
            cod_disc = inscricao["cod_disciplina"]
            semestre = inscricao["semestre"]
            publico = aluno.get("publico_letivo", "veteranos")
            periodo = sia.PERIODOS_LETIVOS.get((semestre, publico))
            if periodo is None:
                continue

            inicio, fim = periodo
            horarios = [
                h for h in sia.TABELA_SIA_HORARIOS_TURMAS
                if h["cod_disciplina"] == cod_disc and h["semestre"] == semestre
            ]
            dias_sem_aula = {
                e["dt_evento"] for e in sia.TABELA_SIA_CALENDARIO
                if e["semestre"] == semestre and e["tipo_evento"] in {"FERIADO", "RECESSO"}
            }
            total_nominal = 0
            aulas_canceladas = 0
            for horario in horarios:
                dia = MAPA_DIAS[horario["dia_semana"]]
                data_aula = inicio + timedelta(days=(dia - inicio.weekday()) % 7)
                while data_aula <= fim:
                    total_nominal += 1
                    aulas_canceladas += data_aula in dias_sem_aula
                    data_aula += timedelta(weeks=1)

            aulas_uteis = total_nominal - aulas_canceladas
            if aulas_uteis == 0:
                continue
            limite_max_faltas = math.floor(aulas_uteis * 0.25)

            faltas_atuais = inscricao["qtd_faltas"]
            perc_faltas = (faltas_atuais / aulas_uteis) * 100
            faltas_restantes = limite_max_faltas - faltas_atuais

            if perc_faltas >= limite_pref or faltas_restantes <= 2:
                print("*" * 65)
                print(f"ALERTA PROATIVO DE FREQUÊNCIA: {aluno['nome_completo']} ({matricula})")
                print(f"Disciplina: {cod_disc} | {total_nominal} aulas - {aulas_canceladas} encontros em feriados ou recessos = {aulas_uteis} úteis.")
                print(f"Teto Institucional (25%): Máx {limite_max_faltas} faltas.")
                print(f"Faltas atuais: {faltas_atuais} ({perc_faltas:.1f}%). Restam apenas: {faltas_restantes} falta(s).")
                print("*" * 65)

def executar_job_ti(data_referencia: date, semestre: str = "2026.2"):
    from plano_operacional import montar_plano

    print(f"[JOB TI] Ações com prazo nos próximos 7 dias a partir de {data_referencia}")
    fim = data_referencia + timedelta(days=7)
    for acao in montar_plano(semestre)["acoes"]:
        prazo = acao["prazo"]
        if prazo is not None and data_referencia <= prazo <= fim:
            print(f"{prazo} | {acao['evento']} | {acao['responsavel']} | {acao['acao']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ti", action="store_true", help="Mostra os próximos prazos do plano de TI")
    parser.add_argument("--data-referencia", type=date.fromisoformat, help="Data no formato AAAA-MM-DD")
    parser.add_argument("--semestre", choices=("2026.1", "2026.2"), default="2026.2", help="Semestre do plano de TI")
    args = parser.parse_args()
    if args.ti:
        executar_job_ti(args.data_referencia or date.today(), args.semestre)
    else:
        executar_job_financeiro(args.data_referencia or date(2026, 2, 8))
        executar_job_academico_faltas()
