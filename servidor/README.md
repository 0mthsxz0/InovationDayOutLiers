# Servidor IBMEC — MVP

Execute a partir desta pasta. O servidor usa FastAPI, dados de demonstração
e um worker com alertas e planos de TI para 2026.1 e 2026.2.

## Windows

Para uma instalação nova, crie o ambiente virtual e instale as dependências.

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Abra o [Swagger local](http://127.0.0.1:8000/docs).

```powershell
.\venv\Scripts\python.exe worker.py
.\venv\Scripts\python.exe worker.py --ti --semestre 2026.1 --data-referencia 2026-06-22
```

O login e a integração autenticada com os chats ainda precisam ser implementados
antes de disponibilizar consultas privadas fora do ambiente local.

## Perfis de demonstração e demanda

Abra http://127.0.0.1:8000/demo/login. O seletor oferece Aluno, Professor,
Equipe de TI e Equipe de Suporte. O login é local e usa contas fictícias.
Para Suporte, o perfil é concedido pela seleção no formulário, com matrícula
e senha fictícias preenchidas. A sessão autoriza as consultas em /demo e
restringe a pesquisa a registros de demonstração. As rotas legadas de
Swagger seguem disponíveis para desenvolvimento local.

A rota GET /demo/ferramentas retorna as prioridades para o perfil da sessão
e os eventos em curso ou a até sete dias. A data de referência pode ser
informada em YYYY-MM-DD. Por exemplo, 2026-11-08 destaca AP2 para o aluno.
As consultas por domínio em /demo/consulta retornam somente o JSON solicitado.

As prioridades são hipóteses baseadas nas datas do calendário e nos fluxos
visíveis no SIA. Para calibrar com o gráfico de demanda, primeiro registre
origem, unidade e granularidade de cada série. Cruze cada janela acadêmica
com as séries e, quando disponível, com contagens agregadas por tipo de
consulta. O volume geral pode indicar janelas para monitorar. Para escolher
quais ferramentas destacar com base em uso observado, são necessárias
contagens por consulta. Acompanhe a quantidade de chamadas por conversa e
o tamanho das respostas antes e depois de aplicar as prioridades.

## Conector MCP do calendário

A partir da pasta servidor, instale as dependências e inicie o aplicativo MCP
em um processo separado da API principal.

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn mcp_calendario:app --host 127.0.0.1 --port 8766
```

Configure um cliente MCP local com Streamable HTTP em
http://127.0.0.1:8766/mcp e chame consultar_calendario com semestre 2026.2.
A resposta deve incluir a aplicação da AP2 de 12 a 18 de novembro.

Para testar em um chat remoto, publique apenas este aplicativo em HTTPS.
Configure o proxy para encaminhar /mcp e usar o Host local aceito pelo SDK.
Depois de validar o endereço externo com um cliente MCP, atualize
../plugin/CONEXAO.md com a URL HTTPS. A API de demonstração por perfil é
executada em outro processo.
