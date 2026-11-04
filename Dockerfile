FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mcp_calendario.py calendario_academico.py models.py mcp_conta.py oauth_mcp_demo.py tarefas_mcp_demo.py dados_mcp_demo.py plano_operacional.py ./
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "mcp_conta:app", "--no-access-log", "--host", "0.0.0.0", "--port", "8080"]
