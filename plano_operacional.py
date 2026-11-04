from datetime import timedelta

from calendario_academico import EVENTOS


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
