# Publicar o calendário do Ibmec Conecta

Este pacote executa somente o conector MCP de calendário. Use uma hospedagem
autorizada com HTTPS e publique a rota /mcp da aplicação.

## Implantação

1. Na hospedagem, use o Dockerfile deste pacote e encaminhe o tráfego para a
   porta 8080. Para usar Python diretamente, instale requirements.txt e execute
   python -m uvicorn mcp_calendario:app --host 0.0.0.0 --port 8080.
2. Se o proxy repassar o Host público, defina IBMEC_MCP_HOST_PUBLICO com o
   domínio exato, sem https:// e sem /mcp. Se o proxy reescrever o Host para
   127.0.0.1:8080, o valor padrão já o aceita.
3. Valide a URL HTTPS com um cliente MCP usando Streamable HTTP e protocolo
   2025-11-25. Liste as ferramentas e confirme consultar_calendario. Chame a
   ferramenta com semestre 2026.2 e confira a AP2 de 12 a 18/11/2026.
4. Copie a URL HTTPS completa, com /mcp, para CONEXAO.md na pasta plugin.

Para testar no Gemini, abra o Gemini Apps Developer Mode, escolha Create new
e informe a URL em MCP Server URL. Confira a ferramenta em Tool schemas e
consulte a AP2 de 2026.2. Este endpoint de calendário dispensa autenticação.
A disponibilidade do modo de desenvolvedor depende da conta.

[Guia oficial do modo de desenvolvedor](https://developers.google.com/connected-apps/mcp/dev-mode/usage)
