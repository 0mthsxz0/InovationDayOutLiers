from datetime import date
from typing import List, Dict, Any

from calendario_academico import TABELA_SIA_CALENDARIO

# Contas de demonstração para o futuro vínculo de identidade do plugin.
TABELA_SIA_PERFIS: List[Dict[str, Any]] = [
    {
        "id_perfil": "suporte-demo",
        "papel": "suporte",
        "nome": "Davi Demo",
        "email": "davi.suporte@example.com",
        "equipe": "Suporte Acadêmico",
    },
    {
        "id_perfil": "aluno-demo-2",
        "papel": "aluno",
        "nome": "Eva Demo",
        "email": "eva.aluno@example.com",
        "matricula": "202602",
    },
    {
        "id_perfil": "aluno-demo",
        "papel": "aluno",
        "nome": "Ana Demo",
        "email": "ana.aluno@example.com",
        "matricula": "202601",
    },
    {
        "id_perfil": "professor-demo",
        "papel": "professor",
        "nome": "Bruno Demo",
        "email": "bruno.professor@example.com",
        "disciplinas": ["CALC1"],
    },
    {
        "id_perfil": "ti-demo",
        "papel": "ti",
        "nome": "Camila Demo",
        "email": "camila.ti@example.com",
        "equipe": "Operações de TI",
    },
]

TABELA_SIA_ALUNOS: List[Dict[str, Any]] = [
    {
        "id_aluno": 102,
        "matricula": "202601",
        "nome_completo": "Ana Demo",
        "cod_curso": "ENG-COMP",
        "nome_curso": "Engenharia",
        "email_institucional": "ana.aluno@example.com",
        "url_reset_senha": "https://example.com/redefinir",
        "cfg_limite_alerta_freq": 19.0,
        "cfg_aviso_aulas_faltantes": None,
    },
    {
        "id_aluno": 103,
        "matricula": "202602",
        "nome_completo": "Eva Demo",
        "cod_curso": "ENG-COMP",
        "nome_curso": "Engenharia",
        "email_institucional": "eva.aluno@example.com",
        "url_reset_senha": "https://example.com/redefinir",
        "cfg_limite_alerta_freq": 19.0,
        "cfg_aviso_aulas_faltantes": None,
    },
    {
        "id_aluno": 101,
        "matricula": "202601040227",
        "nome_completo": "Matheus Milagres Jacob Candian",
        "cod_curso": "ENG-COMP",
        "nome_curso": "Engenharia",
        "email_institucional": "202601040227@alunos.ibmec.edu.br",
        "url_reset_senha": "https://ibmec.br/reset",
        "cfg_limite_alerta_freq": 19.0,
        "cfg_aviso_aulas_faltantes": None
    }
]

TABELA_SIA_TITULOS: List[Dict[str, Any]] = [
    {
        "id_titulo": 5001,
        "matricula_aluno": "202601040227",
        "ano_mes": "2026-02",
        "dt_vencimento": date(2026, 2, 10),
        "vlr_nominal": 2500.00,
        "cod_status": "PENDENTE",
        "cod_barras": "34191.09008 63571.277308 71444.640008 5 900000250000",
        "linha_digitavel": "341910900863571277308714446400085900000250000",
        "url_pix": "https://pix.ibmec.br/payload/123"
    },
    {
        "id_titulo": 5003,
        "matricula_aluno": "202601",
        "ano_mes": "2026-02",
        "dt_vencimento": date(2026, 2, 10),
        "vlr_nominal": 950.00,
        "cod_status": "PENDENTE",
        "cod_barras": "DEMONSTRACAO",
        "linha_digitavel": "DEMONSTRACAO",
        "url_pix": "https://example.com/pix-demonstracao",
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
        "id_matricula_disc": 902,
        "matricula_aluno": "202601",
        "semestre": "2026.1",
        "cod_disciplina": "CALC1",
        "nota_ap1": 8.0,
        "nota_ap2": None,
        "nota_as": None,
        "qtd_faltas": 4,
        "perc_frequencia": 89.7,
    },
    {
        "id_matricula_disc": 903,
        "matricula_aluno": "202602",
        "semestre": "2026.1",
        "cod_disciplina": "CALC1",
        "nota_ap1": 9.0,
        "nota_ap2": None,
        "nota_as": None,
        "qtd_faltas": 4,
        "perc_frequencia": 89.7,
    },
    {
        "id_matricula_disc": 901,
        "matricula_aluno": "202601040227",
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

PERIODOS_LETIVOS = {
    ("2026.1", "veteranos"): (date(2026, 2, 9), date(2026, 7, 3)),
    ("2026.1", "calouros"): (date(2026, 2, 23), date(2026, 7, 3)),
}
