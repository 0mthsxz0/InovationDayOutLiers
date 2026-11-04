from datetime import date
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class PreferenciasNotificacao(BaseModel):
    limite_alerta_frequencia_percentual: float
    aviso_antecedencia_aulas_faltantes: Optional[int] = None

class AlunoSchema(BaseModel):
    matricula: str
    nome: str
    curso: str
    email_institucional: str
    link_recuperacao_senha: HttpUrl
    preferencias_notificacao: PreferenciasNotificacao

class AtualizarPreferenciasRequest(BaseModel):
    limite_alerta_frequencia_percentual: float
    aviso_antecedencia_aulas_faltantes: Optional[int] = None

class MensalidadeSchema(BaseModel):
    mes_referencia: str
    data_vencimento: date
    valor_total: float
    status_pagamento: str
    codigo_barras: str
    linha_digitavel: str
    qr_code_pix_url: HttpUrl

class FinanceiroSchema(BaseModel):
    matricula: str
    mensalidades: List[MensalidadeSchema]

class NotasSchema(BaseModel):
    AP1: Optional[float] = None
    AP2: Optional[float] = None
    AS: Optional[float] = None

class FrequenciaSchema(BaseModel):
    faltas_acumuladas: int
    frequencia_percentual_atual: float

class DisciplinaSchema(BaseModel):
    codigo_disciplina: str
    nome_disciplina: str
    notas: NotasSchema
    frequencia: FrequenciaSchema

class AcademicoSchema(BaseModel):
    matricula: str
    semestre_atual: str
    disciplinas: List[DisciplinaSchema]

class AulaGradeSchema(BaseModel):
    dia_da_semana: str
    horario_inicio: str
    horario_fim: str

class DisciplinaGradeSchema(BaseModel):
    codigo_disciplina: str
    nome_disciplina: str
    aulas: List[AulaGradeSchema]

class GradeSchema(BaseModel):
    matricula: str
    semestre: str
    grade: List[DisciplinaGradeSchema]

class FeriadoRecessoSchema(BaseModel):
    data: date
    descricao: str

class CalendarioSchema(BaseModel):
    semestre_referencia: str
    feriados_e_recessos: List[FeriadoRecessoSchema]
    eventos_academicos: Optional[List['EventoOperacionalSchema']] = None

class EventoOperacionalSchema(BaseModel):
    nome: str
    inicio: date
    fim: date
    tipo: str
    publico: str
    precisao: str
    fonte: str


class AcaoOperacionalSchema(BaseModel):
    evento: str
    servico: str
    acao: str
    prazo: Optional[date]
    responsavel: str
    verificacao: str
    status: str


class SobreposicaoSchema(BaseModel):
    inicio: date
    fim: date
    eventos: List[str]


class PlanoOperacionalSchema(BaseModel):
    semestre: str
    eventos: List[EventoOperacionalSchema]
    acoes: List[AcaoOperacionalSchema]
    sobreposicoes: List[SobreposicaoSchema]
