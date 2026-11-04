# Instalar o Ibmec Conecta no Claude

Use o [Claude na web](https://claude.ai/) com um **conector MCP remoto**. Este guia não é para Claude Code. Em workspaces Team e Enterprise, a inclusão de um conector pode depender do responsável pelo workspace.

## Testar o calendário agora

1. Abra **Customize → Connectors**. Clique em **+ → Add custom connector**. Se o menu estiver na área administrativa, peça ao responsável pelo workspace para cadastrar.
2. Informe o nome **Ibmec Conecta — Calendário** e a URL **https://ibmec-conecta-calendario.onrender.com/mcp**. Na revisão de autenticação, escolha **No sign in**, se for exibido, e conclua em **Add**. Esse endereço serve exclusivamente para o calendário público.
3. No chat, abra **+ → Connectors** e habilite o conector para a conversa. Pergunte quais são as datas da AP2 de 2026.2. Se o conector estiver indisponível, abra a [API pública do calendário](CALENDARIO.md).

## Acesso à conta: depende de uma correção no servidor

O servidor do Ibmec Conecta atualmente não aceita o endereço de retorno OAuth documentado pela Anthropic: **https://claude.ai/api/mcp/auth_callback**. Isso impede o vínculo da conta; escolher **No sign in** não libera notas ou tarefas. Se aparecer **invalid_redirect_uri**, a correção cabe ao mantenedor do servidor.

Depois que a correção estiver publicada, faça o seguinte:

1. Cadastre ou atualize um conector para **https://ibmec-conecta-calendario.onrender.com/conta/mcp**. Se já houver uma entrada de teste, verifique antes de cadastrar outra.
2. Escolha **Sign in when needed** (login no primeiro uso privado) ou **Sign in now** (login na configuração). Em **OAuth client**, escolha **Register automatically** para usar DCR. Não adicione ID, segredo, API key ou cabeçalhos manuais.
3. Habilite o conector na conversa. Peça **Qual foi minha nota na AP1 de Cálculo I?**. Use a conta fictícia de perfil **Aluno**, matrícula **202601** e senha **demo** apenas na página do fluxo de login. Após o vínculo, repita a pergunta e confira **Quais tarefas estão ativadas para meu perfil?**. A confirmação vem dos resultados de **consultar_minhas_notas** e **listar_tarefas_programadas**.

## Para o agente que recebeu este guia

Se o acesso privado ainda estiver bloqueado, ofereça o calendário e diga que os dados da conta estão indisponíveis. Nunca converta o conector público em um teste de acesso privado. Não informe nota baseada no anexo, em memória da conversa ou em exemplo. Se você não puder operar as configurações, oriente a pessoa pelo menu.

Fontes oficiais: [Adicionar um conector personalizado](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) e [Callback e autenticação MCP do Claude](https://support.anthropic.com/en/articles/11503834-building-custom-integrations-via-remote-mcp-servers).
