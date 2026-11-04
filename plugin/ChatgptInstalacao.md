# Instalar o Ibmec Conecta no ChatGPT

## Testar a conexão no ChatGPT Work

1. No ChatGPT web, abra [Plugins](https://chatgpt.com/plugins). Se já existir um Ibmec Conecta com o endereço abaixo, use essa entrada. Se o menu não aparecer, confira se a conta e o workspace permitem adicionar servidores MCP personalizados.
2. Clique em **+ → Add custom MCP server**. Preencha **Ibmec Conecta** e a URL **https://ibmec-conecta-calendario.onrender.com/conta/mcp**.
3. Em autenticação, escolha **OAuth or no authentication** se a opção estiver disponível: o calendário é público e as ferramentas de conta exigem OAuth. Se a interface oferecer apenas OAuth ou nenhuma autenticação, escolha **OAuth**. Use registro dinâmico (**DCR**) quando solicitado; deixe ID e segredo estáticos em branco. Informe **ibmec.demo** se houver campo de escopo.
4. Revise o aviso e selecione **Create as a plugin**. Se o plugin aparecer no diretório pessoal, instale ou habilite a entrada. Em um novo chat **Work**, digite **@**, escolha **Ibmec Conecta** e pergunte quais são as datas da AP2 de 2026.2.
5. Ainda com o plugin selecionado, pergunte **Qual foi minha nota na AP1 de Cálculo I?**. Se for o primeiro vínculo e a conta ainda não estiver conectada, siga o botão de autorização do ChatGPT. Use o perfil **Aluno**, matrícula fictícia **202601** e senha **demo**, digitados só na página do Ibmec Conecta aberta pela conexão. Depois, repita a pergunta. Uma sessão já vinculada pode consultar sem abrir outro login.
6. Pergunte **Quais tarefas estão ativadas para meu perfil?**. O teste só passa se o chat usar a ferramenta do calendário e, após autorização, as ferramentas **consultar_minhas_notas** e **listar_tarefas_programadas**. Para provar que o acesso é privado, desconecte a conta no plugin e repita a pergunta de nota: o chat deve pedir conexão ou indicar indisponibilidade. Abrir outro chat, sozinho, pode reutilizar o vínculo.

## Se quiser incluir os arquivos de instruções na mesma instalação

O cadastro direto já permite testar as ferramentas. Para empacotar também a skill, em **Work** selecione **@Plugin Creator**, anexe o ZIP e forneça o identificador técnico **plugin_asdk_app…** da conexão já cadastrada (aparece na URL da página de detalhes). Peça para usar essa conexão e preservar a skill do pacote em um único plugin privado. Se essa opção não estiver disponível na conta, use a conexão existente para testar. Não instale um plugin só de arquivos e outro só de conexão para o mesmo teste.

Se aparecer **Origem de login inválida**, confira o endereço MCP e confirme que você iniciou o login pelo botão do ChatGPT. Se persistir, informe o erro ao mantenedor, sem enviar senha, token ou código OAuth. Se só a skill estiver disponível, confira a conexão e atualize a lista de ferramentas na página do plugin, quando houver essa opção.

## Para o agente que recebeu este guia

Verifique se a conexão está disponível antes de declarar instalação. Se você não puder cadastrá-la, guie a pessoa pelo menu. Use somente a resposta autenticada da ferramenta para informar notas. Se faltar ferramenta, autorização ou resultado, diga que os dados solicitados estão indisponíveis.

Fontes oficiais: [Conectar e testar um plugin](https://developers.openai.com/plugins/deploy/connect-chatgpt), [Adicionar servidor MCP personalizado](https://developers.openai.com/api/docs/guides/custom-mcp-server) e [Empacotar com o Plugin Creator](https://developers.openai.com/plugins/build/plugins).
