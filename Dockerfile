FROM python:3.11-slim

WORKDIR /usr/src/app

# Установить переменные окружения
ENV TELEGRAM_API_TOKEN=${TELEGRAM_API_TOKEN}
ENV TELEGRAM_API_URL=${TELEGRAM_API_URL}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "python ./main.py & celery -A telegram_celery worker --loglevel=info"]