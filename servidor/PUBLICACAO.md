# Publicar o Ibmec Conecta de demonstração

O serviço usa um único processo e contém somente calendário e contas
fictícias. O Dockerfile inicia o aplicativo na porta 8080. A configuração
do Render usa essa porta e o health check /healthz.

## Endereços

- /mcp oferece a consulta de calendário sem login.
- /conta/mcp oferece calendário, notas fictícias e tarefas da conta após OAuth.
- /entrar abre o formulário quando recebe um fluxo iniciado pelo cliente MCP.

O Render fornece RENDER_EXTERNAL_URL. Em outra hospedagem, configure
IBMEC_ORIGEM_MCP com a origem HTTPS para gerar os endereços OAuth.
Para executar localmente, instale requirements.txt e use
python -m uvicorn mcp_conta:app --host 127.0.0.1 --port 8767.

## Teste autenticado

Conecte /conta/mcp em um cliente que aceite MCP com OAuth. Pergunte pela AP1,
siga o login e volte ao chat. Use a matrícula fictícia 202601, perfil Aluno
e senha demo. Confirme a chamada autenticada à ferramenta de notas. As contas professor-demo, ti-demo e suporte-demo usam a mesma
senha de teste com seus perfis correspondentes. Peça as tarefas programadas
para conferir as regras ativadas.

A agenda grava ativações e avisos em SQLite. Defina IBMEC_TAREFAS_DB para
guardar o arquivo em um volume persistente se houver. O Render gratuito
pode suspender o processo e limpar o disco local. A verificação roda enquanto
o serviço está ativo e ao consultar os avisos. As sessões OAuth ficam em
memória e exigem novo vínculo após reiniciar. Os avisos aparecem na consulta
de tarefas do chat.

Defina IBMEC_OAUTH_CLIENT_KEY como segredo permanente com pelo menos 32 bytes.
Ele permite recuperar novos cadastros de clientes OAuth após reiniciar o
serviço. Preserve o mesmo valor entre deploys.

A rota GET /api/calendario?semestre=2026.2 é pública. Configure IBMEC_CALENDARIO_DB para guardar o SQLite em um volume persistente, quando disponível.
