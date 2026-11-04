from datetime import date
import json
import sia_database as sia
from sia_service import SiaService

print("=== 1. JSON INICIAL GERADO DO BANCO SIA ===")
print(json.dumps(SiaService.montar_json_financeiro("202601"), default=str, indent=2))

print("\n=== 2. EVENTO NO SIA: Pagamento de boleto e emissão de nova fatura ===")
sia.TABELA_SIA_TITULOS[0]["cod_status"] = "PAGO"
sia.TABELA_SIA_TITULOS.append({
    "id_titulo": 5002,
    "matricula_aluno": "202601",
    "ano_mes": "2026-03",
    "dt_vencimento": date(2026, 3, 10),
    "vlr_nominal": 2500.00,
    "cod_status": "PENDENTE",
    "cod_barras": "DEMONSTRACAO",
    "linha_digitavel": "DEMONSTRACAO",
    "url_pix": "https://example.com/pix-demonstracao"
})

print("\n=== 3. NOVO JSON RE-MONTADO PELA API AUTOMATICAMENTE ===")
print(json.dumps(SiaService.montar_json_financeiro("202601"), default=str, indent=2))
