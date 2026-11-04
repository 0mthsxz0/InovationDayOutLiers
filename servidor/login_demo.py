from datetime import date
from secrets import token_urlsafe
from time import monotonic
from typing import Literal
from urllib.parse import parse_qs

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from plano_operacional import EVENTOS
from sia_database import TABELA_SIA_PERFIS
from sia_service import SiaService

router = APIRouter(prefix="/demo", tags=["Demonstração"])
PAPEIS = {"aluno": "Aluno", "professor": "Professor", "ti": "Equipe de TI",
          "suporte": "Equipe de Suporte"}
CONSULTAS = {
    "grade": SiaService.montar_json_grade,
    "academico": SiaService.montar_json_academico,
    "aluno": SiaService.montar_json_aluno,
    "financeiro": SiaService.montar_json_financeiro,
}
SESSOES = {}
COOKIE = "ibmec_demo"
DURACAO = 3600


@router.get("/login", response_class=HTMLResponse)
def pagina_login():
    opcoes = "".join(f'<option value="{papel}">{nome}</option>' for papel, nome in PAPEIS.items())
    return f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8">
    <title>Ibmec Conecta</title><main><h1>Ibmec Conecta</h1>
    <p>Modo demonstração. Use somente dados fictícios.</p>
    <form method="post">
      <p><label>Matrícula <input name="matricula" required></label></p>
      <p><label>Senha <input name="senha" type="password" required></label></p>
      <p><label>Perfil <select name="papel">{opcoes}</select></label></p>
      <button type="submit">Entrar</button>
    </form>
    <p>Aluno: 202601 ou 202602. Professor: professor-demo. TI: ti-demo.
    Senha de teste: demo. Para Suporte, use quaisquer valores fictícios.</p>
    </main></html>"""


@router.post("/login")
async def entrar(request: Request):
    campos = parse_qs((await request.body()).decode("utf-8", errors="replace"))
    papel = campos.get("papel", [""])[0]
    matricula = campos.get("matricula", [""])[0].strip()
    senha = campos.get("senha", [""])[0]
    if papel not in PAPEIS or not matricula or not senha:
        raise HTTPException(400, "Informe matrícula, senha e perfil.")
    perfil = next(
        (p for p in TABELA_SIA_PERFIS
         if p["papel"] == papel and p.get("matricula", p["id_perfil"]) == matricula),
        None,
    )
    if papel == "suporte":
        perfil = next(p for p in TABELA_SIA_PERFIS if p["papel"] == "suporte")
    elif perfil is None or senha != "demo":
        raise HTTPException(401, "Use as credenciais fictícias do perfil escolhido.")

    agora = monotonic()
    for token, (_, expira) in tuple(SESSOES.items()):
        if expira <= agora:
            SESSOES.pop(token, None)
    SESSOES.pop(request.cookies.get(COOKIE), None)
    token = token_urlsafe(32)
    SESSOES[token] = (perfil, agora + DURACAO)
    resposta = RedirectResponse(str(request.url_for("ferramentas_demo")), status_code=303)
    resposta.set_cookie(COOKIE, token, max_age=DURACAO, httponly=True, samesite="lax",
                         secure=request.url.scheme == "https", path="/demo")
    return resposta


def perfil_da_sessao(request: Request):
    sessao = SESSOES.get(request.cookies.get(COOKIE))
    if sessao is None or sessao[1] <= monotonic():
        raise HTTPException(401, "Entre pelo login de demonstração.")
    return sessao[0]


def montar_ferramentas(papel, referencia):
    eventos_proximos = []
    avaliacoes_recentes = []
    for semestre, eventos in EVENTOS.items():
        for evento in eventos:
            ate_inicio = (evento["inicio"] - referencia).days
            desde_fim = (referencia - evento["fim"]).days
            em_curso_ou_proximo = desde_fim <= 0 and ate_inicio <= 7
            avaliacao_recente = evento["tipo"] == "avaliacao" and 1 <= desde_fim <= 7
            if not (em_curso_ou_proximo or avaliacao_recente):
                continue
            fase = "encerrado" if avaliacao_recente else ("proximo" if ate_inicio > 0 else "em_curso")
            contexto = {
                **{campo: evento[campo] for campo in ("nome", "inicio", "fim", "tipo", "precisao")},
                "semestre": semestre,
                "fase": fase,
            }
            if evento["precisao"] == "dia":
                contexto["dias_ate_inicio"] = max(0, ate_inicio)
                contexto["dias_desde_fim"] = max(0, desde_fim)
            if avaliacao_recente:
                avaliacoes_recentes.append(contexto)
            else:
                eventos_proximos.append(contexto)
    prioridades = {
        "aluno": ["grade", "academico", "financeiro", "calendario"],
        "professor": ["calendario"],
        "ti": ["plano_operacional", "calendario"],
        "suporte": ["grade", "academico", "aluno", "financeiro", "calendario"],
    }[papel]
    tipos = {evento["tipo"] for evento in eventos_proximos}
    avaliacoes_em_curso = any(
        evento["tipo"] == "avaliacao" and evento["fase"] == "em_curso"
        for evento in eventos_proximos
    )
    if avaliacoes_em_curso:
        fase_academica = "provas_em_curso"
    elif avaliacoes_recentes:
        fase_academica = "pos_prova"
    elif "avaliacao" in tipos:
        fase_academica = "pre_prova"
    elif tipos.intersection({"notas", "diarios"}):
        fase_academica = "fechamento"
    elif "matricula" in tipos:
        fase_academica = "matricula"
    elif "acolhimento" in tipos:
        fase_academica = "acolhimento"
    else:
        fase_academica = "rotina"

    destaques_aluno = {
        "provas_em_curso": "calendario",
        "pre_prova": "calendario",
        "pos_prova": "academico",
        "fechamento": "academico",
        "matricula": "financeiro",
        "acolhimento": "grade",
    }
    destaque = destaques_aluno.get(fase_academica) if papel == "aluno" else None
    if destaque:
        prioridades.remove(destaque)
        prioridades.insert(0, destaque)
    if papel == "suporte" and fase_academica in {"pre_prova", "provas_em_curso"}:
        prioridades.remove("calendario")
        prioridades.insert(1, "calendario")
    return {
        "papel": papel,
        "referencia": referencia,
        "fase_academica": fase_academica,
        "prioridades": prioridades,
        "eventos_proximos": sorted(eventos_proximos, key=lambda e: e["inicio"]),
        "avaliacoes_recentes": sorted(avaliacoes_recentes, key=lambda e: e["fim"], reverse=True),
    }


@router.get("/ferramentas")
def ferramentas_demo(request: Request, referencia: date | None = None):
    perfil = perfil_da_sessao(request)
    return montar_ferramentas(perfil["papel"], referencia or date.today())


@router.get("/consulta/{dominio}")
def consultar_demo(request: Request, dominio: Literal["grade", "academico", "aluno", "financeiro"],
                   matricula: str | None = None):
    perfil = perfil_da_sessao(request)
    if perfil["papel"] == "aluno":
        if matricula is not None and matricula != perfil["matricula"]:
            raise HTTPException(403, "A sessão de aluno permite apenas a própria matrícula.")
        matricula = perfil["matricula"]
    elif perfil["papel"] != "suporte":
        raise HTTPException(403, "Consulta individual disponível para aluno e suporte.")
    elif not matricula:
        raise HTTPException(422, "Informe a matrícula de demonstração.")

    if not any(p["papel"] == "aluno" and p["matricula"] == matricula for p in TABELA_SIA_PERFIS):
        raise HTTPException(404, "Matrícula ausente da base de demonstração.")
    return CONSULTAS[dominio](matricula)
