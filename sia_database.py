from datetime import date
from typing import List, Dict, Any

TABELA_SIA_ALUNOS: List[Dict[str, Any]] = [
    {
        "id_aluno": 101,
        "matricula": "202601",
        "nome_completo": "Aluno de Demonstração",
        "cod_curso": "ENG-COMP",
        "nome_curso": "Engenharia",
        "email_institucional": "aluno.demo@example.com",
        "url_reset_senha": "https://ibmec.br/reset",
        "cfg_limite_alerta_freq": 19.0,
        "cfg_aviso_aulas_faltantes": None
    }
]

TABELA_SIA_TITULOS: List[Dict[str, Any]] = [
    {
        "id_titulo": 5001,
        "matricula_aluno": "202601",
        "ano_mes": "2026-02",
        "dt_vencimento": date(2026, 2, 10),
        "vlr_nominal": 2500.00,
        "cod_status": "PENDENTE",
        "cod_barras": "DEMONSTRACAO",
        "linha_digitavel": "DEMONSTRACAO",
        "url_pix": "https://example.com/pix-demonstracao"
    }
]

TABELA_SIA_DISCIPLINAS: List[Dict[str, Any]] = [
    {
        "cod_disciplina": "CALC1",
        "nome_disciplina": "Cálculo I",
        "ch_total": 80
    }
]

TABELA_SIA_MATRICULAS_DISCIPLINAS: List[Dict[str, Any]] = [
    {
        "id_matricula_disc": 901,
        "matricula_aluno": "202601",
        "semestre": "2026.1",
        "cod_disciplina": "CALC1",
        "nota_ap1": 8.5,
        "nota_ap2": None,
        "nota_as": None,
        "qtd_faltas": 7,
        "perc_frequencia": 15.5
    }
]

TABELA_SIA_HORARIOS_TURMAS: List[Dict[str, Any]] = [
    {
        "id_horario": 1,
        "cod_disciplina": "CALC1",
        "semestre": "2026.1",
        "dia_semana": "Segunda-feira",
        "hora_inicio": "08:00",
        "hora_fim": "10:00"
    },
    {
        "id_horario": 2,
        "cod_disciplina": "CALC1",
        "semestre": "2026.1",
        "dia_semana": "Quarta-feira",
        "hora_inicio": "10:00",
        "hora_fim": "12:00"
    }
]

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

PERIODOS_LETIVOS = {
    ("2026.1", "veteranos"): (date(2026, 2, 9), date(2026, 7, 3)),
    ("2026.1", "calouros"): (date(2026, 2, 23), date(2026, 7, 3)),
}
