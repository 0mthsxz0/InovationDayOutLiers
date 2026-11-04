# InovationDayOutLiers

MVP Agente Escolar Inteligente para o Innovation Day IBMEC. A API FastAPI usa dados simulados para consultas acadêmicas e financeiras e gera um plano operacional de TI para 2026.1 e 2026.2.

## Executar no Windows

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Abra o [Swagger](http://127.0.0.1:8000/docs). Use a matrícula fictícia `202601` para consultas do aluno. A rota `GET /api/ti/plano-operacional` aceita o parâmetro `semestre`.

## Demonstrar os alertas

```powershell
.\venv\Scripts\python.exe worker.py
.\venv\Scripts\python.exe worker.py --ti --semestre 2026.1 --data-referencia 2026-06-22
```

As definições de ferramentas do Gemini estão em `gemini_tools.json`. Os alertas do worker aparecem no console.
