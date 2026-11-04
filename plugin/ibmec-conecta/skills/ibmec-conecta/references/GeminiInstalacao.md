# Instalar o Ibmec Conecta no Gemini

O caminho abaixo usa o **Gemini normal na web**. Não exige modo de desenvolvedor. Segundo o Google, apps personalizados estão disponíveis em inglês, para maiores de 18 anos nos EUA, com conta pessoal e **Keep Activity** ativado. Contas de trabalho ou escola não são elegíveis. Se o menu não aparecer em uma conta usada no Brasil, anexar o ZIP ou criar um Gem não libera a conexão.

1. Abra [Gemini na web](https://gemini.google.com/). No menu inferior, vá a **Settings → Connected Apps**. Se **Connected Apps** estiver dentro de **Personal Intelligence**, abra por lá.
2. Em **Custom apps**, use o campo para adicionar um link ou clique em **Add a custom app**. Cole **https://ibmec-conecta-calendario.onrender.com/conta/mcp**. Deixe as credenciais avançadas em branco: o servidor oferece registro dinâmico de cliente OAuth (**DCR**).
3. Clique em **Next** e siga as telas de revisão e conexão. Se o Gemini abrir o login do Ibmec Conecta nessa etapa ou no primeiro pedido privado, teste com **Aluno**, matrícula fictícia **202601**, senha **demo**. Digite as credenciais só na página de login aberta pelo fluxo da conexão.
4. Em uma conversa, digite **@** e escolha o app conectado. Pergunte pelas datas da AP2 de 2026.2. Em seguida, pergunte **Qual foi minha nota na AP1 de Cálculo I?** e **Quais tarefas estão ativadas para meu perfil?**. Para confirmar a conexão privada, verifique se o app retornou dados da conta autenticada. Se o vínculo já existir, pode não haver novo pedido de login.

## Se o menu ou a conexão não estiverem disponíveis

- Use o [calendário público](CALENDARIO.md) sem login. Se o chat não puder consultar a API, abra o link no navegador.
- Um erro **Not Acceptable: Client must accept text/event-stream** ao abrir a URL MCP no navegador não é um erro de senha. O endereço é para ser cadastrado em **Custom apps**. Se o erro aparecer no próprio cadastro, envie a mensagem ao mantenedor.
- Sem o conector, dados privados e tarefas da conta ficam indisponíveis.

## Para o agente que recebeu este guia

Confira se **Custom apps** aparece. Se você não tiver acesso às configurações, peça que a pessoa faça os cliques. Só confirme o cadastro depois de testar uma ferramenta. Para notas, use exclusivamente a resposta autenticada de **consultar_minhas_notas**. Para tarefas, use **listar_tarefas_programadas**. Se não tiver a resposta da ferramenta, informe que os dados solicitados estão indisponíveis.

Fonte oficial: [Conectar e gerenciar apps personalizados do Gemini](https://support.google.com/gemini/answer/17209137?hl=en-45).
