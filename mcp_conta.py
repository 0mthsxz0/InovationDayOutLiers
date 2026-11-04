from contextlib import asynccontextmanager
from html import escape
from os import getenv
from secrets import compare_digest
from time import time
from typing import Any, Literal
from urllib.parse import urlparse

import anyio
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import RequestBodyLimitMiddleware, TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Mount

from dados_mcp_demo import ALUNOS, PERFIS
from mcp_calendario import app as calendario_publico
from mcp_calendario import consultar_calendario
from oauth_mcp_demo import OAuthDemo
from tarefas_mcp_demo import TarefasDemo, hoje_local

ORIGEM = (getenv("IBMEC_ORIGEM_MCP") or getenv("RENDER_EXTERNAL_URL") or "http://127.0.0.1:8767").rstrip("/")
RECURSO = ORIGEM + "/conta/mcp"
ESCOPO = "ibmec.demo"
PAPEIS = {"aluno": "Aluno", "professor": "Professor", "ti": "Equipe de TI", "suporte": "Equipe de Suporte"}
DISPONIBILIDADE = "Os dados solicitados não estão disponíveis para eu responder à sua pergunta."
CAMPOS_LOGIN = {
    "Cache-Control": "no-store",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
}
oauth = OAuthDemo(ORIGEM, RECURSO)
tarefas = TarefasDemo(getenv("IBMEC_TAREFAS_DB", "tarefas_demo.sqlite3"))
mcp = FastMCP(
    "Ibmec Conecta — contas de demonstração",
    streamable_http_path="/conta/mcp",
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=[urlparse(ORIGEM).netloc, "127.0.0.1:*", "localhost:*"],
        allowed_origins=[ORIGEM, "https://gemini.google.com"],
    ),
    auth_server_provider=oauth,
    auth=AuthSettings(
        issuer_url=ORIGEM,
        resource_server_url=RECURSO,
        required_scopes=[ESCOPO],
        validate_token_resource=True,
        client_registration_options=ClientRegistrationOptions(
            enabled=True, valid_scopes=[ESCOPO], default_scopes=[ESCOPO],
        ),
        revocation_options=RevocationOptions(enabled=True),
    ),
)
LEITURA = ToolAnnotations(readOnlyHint=True, destructiveHint=False)
mcp.add_tool(consultar_calendario, annotations=LEITURA)


def pagina_login(fluxo, erro="", status=200):
    opcoes = "".join(f'<option value="{codigo}">{nome}</option>' for codigo, nome in PAPEIS.items())
    return HTMLResponse(f"""<!doctype html><html lang="pt-BR">
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ibmec Conecta — Entrar</title>
<main>
<h1>Entrar no Ibmec Conecta</h1>
<p>Ambiente de demonstração. Use uma conta fictícia. O cliente autorizado
poderá consultar dados de demonstração e os avisos do seu perfil.</p>
<p role="alert">{escape(erro)}</p>
<form method="post" action="/entrar">
<input type="hidden" name="fluxo" value="{escape(fluxo, quote=True)}">
<p><label>Matrícula ou ID <input name="identidade" autocomplete="username" required></label></p>
<p><label>Senha <input name="senha" type="password" autocomplete="current-password" required></label></p>
<p><label>Perfil <select name="papel">{opcoes}</select></label></p>
<button type="submit">Entrar e autorizar</button>
</form>
<p>Aluno 202601 ou 202602. Professor professor-demo. TI ti-demo.
Suporte suporte-demo. Senha de demonstração demo.</p>
</main></html>""", status_code=status, headers=CAMPOS_LOGIN)


@mcp.custom_route("/entrar", methods=["GET", "POST"], include_in_schema=False)
async def entrar(request):
    if request.method == "GET":
        fluxo = request.query_params.get("fluxo", "")
        pedido = oauth.pedidos.get(fluxo)
        if pedido is None or pedido.expira <= time():
            return HTMLResponse(
                "Inicie ou refaça a conexão no chat para abrir um novo login.",
                status_code=400, headers=CAMPOS_LOGIN,
            )
        return pagina_login(fluxo)

    if request.headers.get("origin", ORIGEM) != ORIGEM:
        return HTMLResponse("Origem de login inválida.", status_code=403, headers=CAMPOS_LOGIN)
    async with request.form(max_fields=5, max_files=0, max_part_size=1024) as campos:
        fluxo = campos.get("fluxo", "")
        identidade = campos.get("identidade", "")
        senha = campos.get("senha", "")
        papel = campos.get("papel", "")
        if not all(isinstance(campo, str) for campo in (fluxo, identidade, senha, papel)):
            return HTMLResponse("Formulário inválido.", status_code=400, headers=CAMPOS_LOGIN)
        pedido = oauth.pedidos.get(fluxo)
        if pedido is None or pedido.expira <= time():
            return HTMLResponse("Login expirado. Reabra o login pelo chat.", status_code=400, headers=CAMPOS_LOGIN)
        if papel not in PAPEIS or PERFIS.get(identidade) != papel or not compare_digest(senha.encode(), b"demo"):
            return pagina_login(fluxo, "Confira a conta, a senha de demonstração e o perfil.", 401)
        # A autorização e a ativação usam a mesma conta validada no formulário.
        tarefas.ativar(identidade, hoje_local())
        destino = oauth.concluir(fluxo, identidade)
        return RedirectResponse(destino, status_code=303, headers=CAMPOS_LOGIN)


def identidade_autorizada():
    token = get_access_token()
    if token is None or token.subject not in PERFIS:
        raise ValueError("Entre com uma conta de demonstração.")
    return token.subject


def notas_do_aluno(matricula, avaliacao):
    dados = ALUNOS[matricula]["notas"]
    notas = []
    for disciplina in dados["disciplinas"]:
        avaliacoes = {
            nome: valor for nome, valor in disciplina["notas"].items()
            if valor is not None and (avaliacao is None or nome == avaliacao)
        }
        if avaliacoes:
            notas.append({"disciplina": disciplina["nome_disciplina"], "notas": avaliacoes})
    if not notas:
        return {"dados_disponiveis": False, "mensagem": DISPONIBILIDADE}
    return {"dados_disponiveis": True, "demonstracao": True, "semestre": dados["semestre_atual"],
            "disciplinas": notas}


@mcp.tool(annotations=LEITURA)
def consultar_minhas_notas(avaliacao: Literal["AP1", "AP2", "AS"] | None = None) -> dict[str, Any]:
    """Consulta as notas fictícias do aluno autenticado. Nenhuma matrícula é informada pelo chat."""
    identidade = identidade_autorizada()
    if PERFIS[identidade] != "aluno":
        return {"dados_disponiveis": False, "mensagem": DISPONIBILIDADE}
    return notas_do_aluno(identidade, avaliacao)


@mcp.tool(annotations=LEITURA)
def consultar_notas_de_suporte(matricula: Literal["202601", "202602"],
                              avaliacao: Literal["AP1", "AP2", "AS"] | None = None) -> dict[str, Any]:
    """Consulta notas de uma matrícula fictícia, apenas para a equipe de Suporte autenticada."""
    if PERFIS[identidade_autorizada()] != "suporte":
        return {"dados_disponiveis": False, "mensagem": DISPONIBILIDADE}
    return notas_do_aluno(matricula, avaliacao)


@mcp.tool(annotations=LEITURA)
def listar_tarefas_programadas() -> dict[str, Any]:
    """Lista as regras ativadas no primeiro login e os avisos da conta autenticada."""
    return tarefas.listar(identidade_autorizada(), hoje_local())


async def verificar_prazos():
    while True:
        await anyio.to_thread.run_sync(tarefas.processar, hoje_local())
        await anyio.sleep(60)


app = mcp.streamable_http_app()
app.router.routes.append(Mount("/", app=calendario_publico))
app.add_middleware(RequestBodyLimitMiddleware, max_body_size=32768)
lifespan_calendario = calendario_publico.router.lifespan_context


@asynccontextmanager
async def lifespan(app):
    tarefas.preparar()
    async with lifespan_calendario(calendario_publico), mcp.session_manager.run(), anyio.create_task_group() as grupo:
        grupo.start_soon(verificar_prazos)
        try:
            yield
        finally:
            grupo.cancel_scope.cancel()


app.router.lifespan_context = lifespan
