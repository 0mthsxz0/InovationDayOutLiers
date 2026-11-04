from dataclasses import dataclass
from re import fullmatch
from secrets import compare_digest, token_urlsafe
from time import time
from urllib.parse import urlparse

from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    AuthorizeError,
    RefreshToken,
    RegistrationError,
    TokenError,
    construct_redirect_uri,
)
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

CALLBACKS_GOOGLE = {
    "oauth-redirect.googleusercontent.com",
    "oauth-redirect-sandbox.googleusercontent.com",
    "oauth-redirect-test.googleusercontent.com",
}


@dataclass
class PedidoLogin:
    client_id: str
    params: AuthorizationParams
    expira: float


class OAuthDemo:
    """Emissor OAuth para as contas fictícias, com sessão em um único processo."""

    def __init__(self, origem: str, recurso: str):
        self.origem = origem
        self.recurso = recurso
        self.clientes: dict[str, OAuthClientInformationFull] = {}
        self.pedidos: dict[str, PedidoLogin] = {}
        self.codigos: dict[str, AuthorizationCode] = {}
        self.acessos: dict[str, AccessToken] = {}
        self.renovacoes: dict[str, RefreshToken] = {}
        self.pares: dict[str, str] = {}

    async def get_client(self, client_id):
        return self.clientes.get(client_id)

    async def register_client(self, client_info):
        for uri in client_info.redirect_uris or []:
            destino = urlparse(str(uri))
            google = (
                destino.scheme == "https" and destino.netloc in CALLBACKS_GOOGLE
                and destino.path.startswith(("/r/", "/a/"))
            )
            chatgpt = (
                destino.scheme == "https"
                and destino.netloc == "chatgpt.com"
                and (
                    destino.path == "/connector_platform_oauth_redirect"
                    or fullmatch(r"/connector/oauth/[A-Za-z0-9_-]+", destino.path) is not None
                )
            )
            local = (
                urlparse(self.origem).hostname in {"127.0.0.1", "localhost"}
                and destino.scheme == "http" and destino.hostname in {"127.0.0.1", "localhost"}
            )
            if destino.fragment or not (google or chatgpt or local):
                raise RegistrationError("invalid_redirect_uri", "Use um callback autorizado.")
        if len(self.clientes) >= 2000:
            raise RegistrationError("invalid_client_metadata", "Limite de clientes da demonstração.")
        self.clientes[client_info.client_id] = client_info

    async def authorize(self, client, params):
        if params.resource and params.resource != self.recurso:
            raise AuthorizeError("invalid_request", "O recurso solicitado não corresponde ao conector.")
        agora = time()
        self.pedidos = {chave: p for chave, p in self.pedidos.items() if p.expira > agora}
        self.codigos = {chave: c for chave, c in self.codigos.items() if c.expires_at > agora}
        if len(self.pedidos) >= 1000:
            raise AuthorizeError("temporarily_unavailable", "Tente novamente mais tarde.")
        fluxo = token_urlsafe(32)
        self.pedidos[fluxo] = PedidoLogin(client.client_id, params, agora + 600)
        return construct_redirect_uri(self.origem + "/entrar", fluxo=fluxo)

    def concluir(self, fluxo, identidade):
        pedido = self.pedidos.pop(fluxo)
        params = pedido.params
        codigo = token_urlsafe(32)
        self.codigos[codigo] = AuthorizationCode(
            code=codigo, client_id=pedido.client_id, scopes=params.scopes or ["ibmec.demo"],
            expires_at=time() + 120, code_challenge=params.code_challenge,
            redirect_uri=params.redirect_uri,
            redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
            resource=params.resource, subject=identidade,
        )
        return construct_redirect_uri(str(params.redirect_uri), code=codigo, state=params.state)

    async def load_authorization_code(self, client, authorization_code):
        codigo = self.codigos.get(authorization_code)
        if codigo and compare_digest(codigo.client_id, client.client_id):
            return codigo
        return None

    async def exchange_authorization_code(self, client, authorization_code):
        if self.codigos.pop(authorization_code.code, None) is None:
            raise TokenError("invalid_grant", "Código já utilizado.")
        return self.emitir(client.client_id, authorization_code.subject, authorization_code.scopes)

    def emitir(self, client_id, identidade, escopos):
        agora = int(time())
        expirados = [r for r in self.renovacoes.values() if r.expires_at <= agora]
        for renovacao in expirados:
            self.remover(renovacao.token)
        acesso, renovacao = token_urlsafe(32), token_urlsafe(32)
        self.acessos[acesso] = AccessToken(
            token=acesso, client_id=client_id, subject=identidade, scopes=escopos,
            expires_at=agora + 3600, resource=self.recurso,
        )
        self.renovacoes[renovacao] = RefreshToken(
            token=renovacao, client_id=client_id, subject=identidade, scopes=escopos,
            expires_at=agora + 7 * 86400, resource=self.recurso,
        )
        self.pares[acesso] = renovacao
        self.pares[renovacao] = acesso
        return OAuthToken(access_token=acesso, refresh_token=renovacao, expires_in=3600, scope=" ".join(escopos))

    async def load_access_token(self, token):
        acesso = self.acessos.get(token)
        return acesso if acesso and acesso.expires_at > time() else None

    async def load_refresh_token(self, client, refresh_token):
        renovacao = self.renovacoes.get(refresh_token)
        if renovacao and renovacao.client_id == client.client_id and renovacao.expires_at > time():
            return renovacao
        return None

    async def exchange_refresh_token(self, client, refresh_token, scopes):
        if refresh_token.token not in self.renovacoes:
            raise TokenError("invalid_grant", "Token de renovação já utilizado.")
        self.remover(refresh_token.token)
        return self.emitir(client.client_id, refresh_token.subject, scopes or refresh_token.scopes)

    def remover(self, token):
        par = self.pares.pop(token, None)
        self.acessos.pop(token, None)
        self.renovacoes.pop(token, None)
        if par:
            self.pares.pop(par, None)
            self.acessos.pop(par, None)
            self.renovacoes.pop(par, None)

    async def revoke_token(self, token):
        self.remover(token.token)
