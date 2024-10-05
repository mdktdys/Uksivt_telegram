#!/bin/bash

# Запуск Python-скрипта в фоновом режиме
python main.py &

# Запуск Celery worker в фоновом режиме
celery -A telegram_celery worker --loglevel=info --pool=solo &
