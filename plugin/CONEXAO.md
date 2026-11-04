# Conexão do Ibmec Conecta

Para consultar o calendário sem login, siga o link da API pública em CALENDARIO.md.
Para consultar notas e tarefas fictícias, conecte o endereço autenticado.

| Uso | URL HTTPS |
|---|---|
| Conta de demonstração, notas e tarefas | https://ibmec-conecta-calendario.onrender.com/conta/mcp |
| Calendário sem login | https://ibmec-conecta-calendario.onrender.com/mcp |

O transporte é MCP Streamable HTTP. O endereço de conta usa OAuth com PKCE.
O cliente descobre o login e faz a troca do código. A pessoa digita a senha
apenas na página de login aberta pelo cliente.

## Teste no Gemini com conta vinculada

1. No Gemini web, abra Configurações e Apps conectados. Se a conta oferecer
   Apps personalizados, adicione a URL autenticada da tabela.
2. Escolha o Ibmec Conecta e peça a nota da AP1. Se o Gemini pedir login
   durante a configuração do app, conclua o vínculo nesse momento.
   Quando o login abrir, selecione Aluno e use matrícula 202601 e senha demo.
3. Após autorizar, volte ao chat e pergunte pela AP1 de Cálculo I. Confirme
   que houve uma chamada bem-sucedida a consultar_minhas_notas. O resultado
   vem da conta autenticada e o valor não está nos guias.
4. Peça para ver suas tarefas programadas. Confira o perfil e as regras
   retornadas por listar_tarefas_programadas.

Use somente as credenciais fictícias acima. Para os outros perfis, use
professor-demo, ti-demo ou suporte-demo com a senha demo e selecione o
perfil correspondente. O login ativa as regras do perfil. O professor
recebe regras de provas e notas, TI de janelas operacionais, Suporte de
revisão de grades e o aluno de boletos e faltas.

Os avisos ficam na lista consultada pelo chat. O plano gratuito do Render
pode suspender o processo e apagar o estado local após reiniciar. Se a
sessão cair, conecte a conta novamente.

[Guia oficial de apps personalizados do Gemini](https://support.google.com/gemini/answer/17209137?hl=en-12)
