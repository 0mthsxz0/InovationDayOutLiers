from fastapi import FastAPI, HTTPException, status
from models import (
    AlunoSchema,
    AtualizarPreferenciasRequest,
    FinanceiroSchema,
    AcademicoSchema,
    GradeSchema,
    CalendarioSchema,
    PlanoOperacionalSchema,
)
from typing import Literal
from login_demo import router as demo_router
from plano_operacional import montar_plano
from sia_service import SiaService

app = FastAPI(
    title="Agente Escolar Inteligente IBMEC - API com Banco SIA Dinâmico",
    description="Camada de serviços que transforma dados do SIA em tempo real nos JSONs do contrato.",
    version="2.0.0"
)

app.include_router(demo_router)


@app.get("/api/aluno/{matricula}", response_model=AlunoSchema, tags=["Aluno"])
def obter_dados_aluno(matricula: str):
    dados = SiaService.montar_json_aluno(matricula)
    if not dados:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não localizado no SIA.")
    return dados

@app.post("/api/aluno/{matricula}/preferencias", response_model=AlunoSchema, tags=["Aluno"])
def atualizar_preferencias_aluno(matricula: str, dados: AtualizarPreferenciasRequest):
    sucesso = SiaService.atualizar_preferencias_aluno(
        matricula,
        dados.limite_alerta_frequencia_percentual,
        dados.aviso_antecedencia_aulas_faltantes
    )
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não localizado no SIA.")
    return SiaService.montar_json_aluno(matricula)

@app.get("/api/financeiro/{matricula}", response_model=FinanceiroSchema, tags=["Financeiro"])
def obter_dados_financeiro(matricula: str):
    dados = SiaService.montar_json_financeiro(matricula)
    if dados is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dados financeiros não localizados.")
    return dados

@app.get("/api/academico/{matricula}", response_model=AcademicoSchema, tags=["Acadêmico"])
def obter_dados_academico(matricula: str):
    dados = SiaService.montar_json_academico(matricula)
    if dados is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Histórico acadêmico não localizado.")
    return dados

@app.get("/api/grade/{matricula}", response_model=GradeSchema, tags=["Grade Horária"])
def obter_grade_aluno(matricula: str):
    dados = SiaService.montar_json_grade(matricula)
    if dados is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade horária não localizada.")
    return dados

@app.get("/api/calendario", response_model=CalendarioSchema, response_model_exclude_none=True, tags=["Calendário"])
def obter_calendario(semestre: Literal["2026.1", "2026.2"] = "2026.1"):
    return SiaService.montar_json_calendario(semestre)


@app.get("/api/ti/plano-operacional", response_model=PlanoOperacionalSchema, tags=["TI"])
def obter_plano_operacional(semestre: Literal["2026.1", "2026.2"] = "2026.2"):
    return montar_plano(semestre)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
