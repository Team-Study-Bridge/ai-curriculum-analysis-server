FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI라면 (main.py에서 app 객체 노출)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]