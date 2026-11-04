from typing import Optional, Dict, Any
import sia_database as sia

class SiaService:

    @staticmethod
    def montar_json_aluno(matricula: str) -> Optional[Dict[str, Any]]:
        aluno = next((a for a in sia.TABELA_SIA_ALUNOS if a["matricula"] == matricula), None)
        if not aluno:
            return None

        return {
            "matricula": aluno["matricula"],
            "nome": aluno["nome_completo"],
            "curso": aluno["nome_curso"],
            "email_institucional": aluno["email_institucional"],
            "link_recuperacao_senha": aluno["url_reset_senha"],
            "preferencias_notificacao": {
                "limite_alerta_frequencia_percentual": aluno["cfg_limite_alerta_freq"],
                "aviso_antecedencia_aulas_faltantes": aluno["cfg_aviso_aulas_faltantes"]
            }
        }

    @staticmethod
    def atualizar_preferencias_aluno(matricula: str, limite_percentual: float, aviso_aulas: Optional[int]) -> bool:
        aluno = next((a for a in sia.TABELA_SIA_ALUNOS if a["matricula"] == matricula), None)
        if not aluno:
            return False

        aluno["cfg_limite_alerta_freq"] = limite_percentual
        aluno["cfg_aviso_aulas_faltantes"] = aviso_aulas
        return True

    @staticmethod
    def montar_json_financeiro(matricula: str) -> Optional[Dict[str, Any]]:
        titulos = [t for t in sia.TABELA_SIA_TITULOS if t["matricula_aluno"] == matricula]
        if not titulos:
            if not any(a["matricula"] == matricula for a in sia.TABELA_SIA_ALUNOS):
                return None

        mensalidades = [
            {
                "mes_referencia": t["ano_mes"],
                "data_vencimento": t["dt_vencimento"],
                "valor_total": t["vlr_nominal"],
                "status_pagamento": t["cod_status"],
                "codigo_barras": t["cod_barras"],
                "linha_digitavel": t["linha_digitavel"],
                "qr_code_pix_url": t["url_pix"]
            }
            for t in titulos
        ]

        return {"matricula": matricula, "mensalidades": mensalidades}

    @staticmethod
    def montar_json_academico(matricula: str, semestre: str = "2026.1") -> Optional[Dict[str, Any]]:
        inscricoes = [
            m for m in sia.TABELA_SIA_MATRICULAS_DISCIPLINAS
            if m["matricula_aluno"] == matricula and m["semestre"] == semestre
        ]
        if not inscricoes:
            if not any(a["matricula"] == matricula for a in sia.TABELA_SIA_ALUNOS):
                return None

        disciplinas = []
        for reg in inscricoes:
            disc_info = next((d for d in sia.TABELA_SIA_DISCIPLINAS if d["cod_disciplina"] == reg["cod_disciplina"]), None)
            nome_disc = disc_info["nome_disciplina"] if disc_info else reg["cod_disciplina"]

            disciplinas.append({
                "codigo_disciplina": reg["cod_disciplina"],
                "nome_disciplina": nome_disc,
                "notas": {
                    "AP1": reg["nota_ap1"],
                    "AP2": reg["nota_ap2"],
                    "AS": reg["nota_as"]
                },
                "frequencia": {
                    "faltas_acumuladas": reg["qtd_faltas"],
                    "frequencia_percentual_atual": reg["perc_frequencia"]
                }
            })

        return {"matricula": matricula, "semestre_atual": semestre, "disciplinas": disciplinas}

    @staticmethod
    def montar_json_grade(matricula: str, semestre: str = "2026.1") -> Optional[Dict[str, Any]]:
        inscricoes = [
            m for m in sia.TABELA_SIA_MATRICULAS_DISCIPLINAS
            if m["matricula_aluno"] == matricula and m["semestre"] == semestre
        ]
        if not inscricoes:
            if not any(a["matricula"] == matricula for a in sia.TABELA_SIA_ALUNOS):
                return None

        grade = []
        for reg in inscricoes:
            cod_disc = reg["cod_disciplina"]
            disc_info = next((d for d in sia.TABELA_SIA_DISCIPLINAS if d["cod_disciplina"] == cod_disc), None)
            nome_disc = disc_info["nome_disciplina"] if disc_info else cod_disc

            horarios = [
                h for h in sia.TABELA_SIA_HORARIOS_TURMAS
                if h["cod_disciplina"] == cod_disc and h["semestre"] == semestre
            ]

            aulas = [
                {
                    "dia_da_semana": h["dia_semana"],
                    "horario_inicio": h["hora_inicio"],
                    "horario_fim": h["hora_fim"]
                }
                for h in horarios
            ]

            grade.append({
                "codigo_disciplina": cod_disc,
                "nome_disciplina": nome_disc,
                "aulas": aulas
            })

        return {"matricula": matricula, "semestre": semestre, "grade": grade}

    @staticmethod
    def montar_json_calendario(semestre: str = "2026.1") -> Dict[str, Any]:
        eventos = [e for e in sia.TABELA_SIA_CALENDARIO if e["semestre"] == semestre]
        return {
            "semestre_referencia": semestre,
            "feriados_e_recessos": [
                {"data": e["dt_evento"], "descricao": e["descricao_evento"]}
                for e in eventos
            ]
        }
