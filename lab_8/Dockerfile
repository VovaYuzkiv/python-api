FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8700

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8700"]
