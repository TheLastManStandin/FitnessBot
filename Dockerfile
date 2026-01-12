FROM python:3.10-slim

WORKDIR /app

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Переменные окружения по умолчанию
ENV RABBITMQ_URL=amqp://rabbitmq:5672

# Команда по умолчанию для запуска FastAPI
CMD ["uvicorn", "src.fast_api.main:app", "--host", "0.0.0.0", "--port", "8000"]