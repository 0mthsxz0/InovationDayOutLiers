FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mcp_calendario.py calendario_academico.py models.py ./
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "mcp_calendario:app", "--host", "0.0.0.0", "--port", "8080"]
