from datetime import date, timedelta

FONTE = "Capturas do Innovation Day IBMEC, calendário 2026.2"


def evento(nome, inicio, fim, tipo, publico, precisao="dia", fonte=FONTE):
    return dict(nome=nome, inicio=date.fromisoformat(inicio), fim=date.fromisoformat(fim),
                tipo=tipo, publico=publico, precisao=precisao, fonte=fonte)


FONTE_2026_1 = "Imagem do Calendário Acadêmico IBMEC 2026.1 (campus e versão não identificados)"

EVENTOS = {
    "2026.1": [
        evento("Abertura da renovação e alteração de disciplinas", "2026-01-20", "2026-01-20",
               "matricula", "Alunos", fonte=FONTE_2026_1),
        evento("Início das aulas de veteranos", "2026-02-09", "2026-02-09",
               "acolhimento", "Veteranos", fonte=FONTE_2026_1),
        evento("Início das aulas de calouros", "2026-02-23", "2026-02-23",
               "acolhimento", "Calouros", fonte=FONTE_2026_1),
        evento("Aplicação da AP1", "2026-04-13", "2026-04-17",
               "avaliacao", "Alunos e docentes", fonte=FONTE_2026_1),
        evento("Fechamento da AP1", "2026-04-30", "2026-04-30",
               "notas", "Docentes e Secretaria", fonte=FONTE_2026_1),
        evento("Aplicação da AP2", "2026-06-11", "2026-06-17",
               "avaliacao", "Alunos e docentes", fonte=FONTE_2026_1),
        evento("Aplicação das avaliações substitutivas", "2026-06-23", "2026-06-30",
               "avaliacao", "Alunos e docentes", fonte=FONTE_2026_1),
        evento("Fechamento dos diários de frequência", "2026-07-01", "2026-07-01",
               "diarios", "Docentes e Secretaria", fonte=FONTE_2026_1),
    ],
    "2026.2": [
        evento("Matrícula e rematrícula", "2026-07-01", "2026-07-31", "matricula", "Alunos", "mes"),
        evento("Início das aulas de veteranos", "2026-08-03", "2026-08-03", "acolhimento", "Veteranos"),
        evento("Início das aulas de calouros", "2026-08-10", "2026-08-10", "acolhimento", "Calouros"),
        evento("Prazo final para trancamento", "2026-10-09", "2026-10-09", "matricula", "Alunos"),
        evento("Fechamento da AP1", "2026-10-13", "2026-10-13", "notas", "Docentes e Secretaria"),
        evento("Aplicação da AP2", "2026-11-12", "2026-11-18", "avaliacao", "Alunos e docentes"),
        evento("Prazo final de notas da AC", "2026-11-16", "2026-11-16", "notas", "Docentes e Secretaria"),
        evento("Lançamento de notas da AP2", "2026-11-23", "2026-11-23", "notas", "Docentes e Secretaria"),
        evento("Bancas de TCC e monografia", "2026-11-23", "2026-11-28", "bancas", "Alunos e docentes"),
        evento("Avaliações substitutivas", "2026-11-25", "2026-12-03", "avaliacao", "Alunos e docentes"),
        evento("Vestibular 2027.1", "2026-11-27", "2026-11-28", "vestibular", "Candidatos"),
    ],
}

REGRAS = {
    "diarios": ("SIA acadêmico", "Validar revisão de notas e fechamento dos diários de frequência.",
                "Sustentação acadêmica e Secretaria", "Fechamento testado e cobertura confirmada", 5),
    "matricula": ("Portal e SIA", "Testar os fluxos da janela e acompanhar erros e chamados.",
                  "Sustentação do portal", "Fluxos validados e erros monitorados", 15),
    "acolhimento": ("Acesso institucional e Wi-Fi", "Validar acesso, recuperação de senha e rede nos campi.",
                    "Service Desk e Redes", "Checklist concluído por campus", 10),
    "notas": ("SIA acadêmico", "Validar lançamento de notas e alinhar escalonamento com a Secretaria.",
              "Sustentação acadêmica e Secretaria", "Fluxo validado e incidentes registrados", 5),
    "avaliacao": ("LMS e suporte", "Testar acesso às avaliações e preparar cobertura do Service Desk.",
                  "Sustentação do LMS", "Acesso validado e cobertura confirmada", 5),
    "bancas": ("Salas e videoconferência", "Validar salas, equipamentos e links das bancas.",
               "Suporte de campus", "Checklist de salas e links concluído", 5),
    "vestibular": ("Portal do candidato e rede", "Validar acesso e confirmar suporte na janela.",
                   "Operações de TI", "Acesso validado e escala confirmada", 5),
}


def montar_plano(semestre):
    eventos = EVENTOS.get(semestre, [])
    acoes = []
    for item in eventos:
        servico, acao, responsavel, verificacao, dias = REGRAS[item["tipo"]]
        # A referência mensal de julho não informa a data exata de abertura.
        prazo = item["inicio"] - timedelta(days=dias) if item["precisao"] == "dia" else None
        acoes.append(dict(evento=item["nome"], servico=servico, acao=acao, prazo=prazo,
                          responsavel=responsavel, verificacao=verificacao, status="proposta"))

    dia = timedelta(days=1)
    datados = [item for item in eventos if item["precisao"] == "dia"]
    limites = sorted({data for item in datados for data in (item["inicio"], item["fim"] + dia)})
    sobreposicoes = []
    for inicio, limite in zip(limites, limites[1:]):
        ativos = [item["nome"] for item in datados if item["inicio"] <= inicio <= item["fim"]]
        if len(ativos) > 1:
            sobreposicoes.append(dict(inicio=inicio, fim=limite - dia, eventos=ativos))
    return dict(semestre=semestre, eventos=eventos, acoes=acoes, sobreposicoes=sobreposicoes)
