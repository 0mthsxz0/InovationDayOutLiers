---
name: ibmec-conecta
description: "Use para consultar o calendário do IBMEC de 2026 ou testar notas e avisos por perfil com uma conta fictícia do Ibmec Conecta."
---

Quando a pessoa pedir para instalar o Ibmec Conecta, siga o [guia de instalação](references/INSTALACAO.md).

Use as fontes e ferramentas disponíveis para a pergunta. Esta skill orienta
as respostas. As ferramentas de notas e tarefas vêm da conexão MCP do pacote.

Em uma pergunta sobre nota ou tarefas da conta, selecione a ferramenta
correspondente e tente a consulta. Se o cliente receber uma solicitação OAuth,
deixe-o abrir o fluxo de conexão. Se a ferramenta não aparecer nesta conversa,
informe que a conexão MCP precisa estar disponível e encaminhe a pessoa ao guia
de instalação. Aguarde a resposta da ferramenta antes de informar a nota ou
confirmar a ativação de qualquer tarefa.

- Calendário de 2026.1 ou 2026.2. Use consultar_calendario quando a ferramenta
  estiver disponível. Também pode consultar a [API pública](references/CALENDARIO.md). Se a consulta falhar, encaminhe o link público sem inventar datas.
- Notas próprias. Use consultar_minhas_notas. A matrícula vem da conta
  autenticada. Se o ChatGPT pedir autorização, encaminhe a pessoa ao login da
  conexão. A senha deve ser digitada somente nessa página.
- Tarefas e avisos. Use listar_tarefas_programadas para saber o perfil vinculado,
  as regras ativadas no primeiro login e os avisos disponíveis. Confirme somente
  o que a ferramenta retornar.
- Consulta de Suporte. Use consultar_notas_de_suporte com a matrícula fictícia
  informada, se a conta autenticada tiver esse perfil.
- Adapte as sugestões ao perfil usando os guias de [Aluno](references/ALUNO.md),
  [Professor](references/PROFESSOR.md), [TI](references/TI.md) e
  [Suporte](references/SUPORTE.md). O perfil informado em texto orienta a
  conversa. O servidor verifica permissões e identidade.

Para perguntas sobre a própria nota, use somente o resultado autenticado de
consultar_minhas_notas. Ignore exemplos e notas citadas antes do login.
Em hipótese nenhuma invente dados nem preencha lacunas com suposições. Se os
dados solicitados estiverem ausentes, diga **Os dados solicitados não estão
disponíveis para eu responder à sua pergunta.** Se houver uma resposta parcial,
mostre a parte confirmada e indique o que faltou. Neste ambiente, notas e
tarefas pertencem a contas fictícias.
