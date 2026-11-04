import anyio

from os import getenv
from typing import Literal

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse

from models import CalendarioSchema
from calendario_academico import montar_json_calendario

host_publico = getenv("IBMEC_MCP_HOST_PUBLICO") or getenv("RENDER_EXTERNAL_HOSTNAME")
hosts_permitidos = ["127.0.0.1:*", "localhost:*", "[::1]:*"]
if host_publico:
    hosts_permitidos.append(host_publico)

mcp = FastMCP(
    "Ibmec Conecta",
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=hosts_permitidos,
        allowed_origins=["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"],
    ),
)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
def consultar_calendario(semestre: Literal["2026.1", "2026.2"]) -> CalendarioSchema:
    """Consulta datas e eventos do calendário acadêmico do semestre informado."""
    return CalendarioSchema.model_validate(montar_json_calendario(semestre))


@mcp.custom_route("/healthz", methods=["GET"], include_in_schema=False)
async def verificar_saude(request):
    return JSONResponse({"status": "ok"})


@mcp.custom_route("/api/calendario", methods=["GET"])
async def calendario_http(request):
    semestre = request.query_params.get("semestre", "2026.1")
    if semestre not in ("2026.1", "2026.2"):
        return JSONResponse({"detail": "Semestre indisponível."}, status_code=422)
    calendario = await anyio.to_thread.run_sync(consultar_calendario, semestre)
    return JSONResponse(calendario.model_dump(mode="json", exclude_none=True))


app = mcp.streamable_http_app()
