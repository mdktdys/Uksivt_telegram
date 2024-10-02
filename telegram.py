import asyncio

from celery import Celery
from utils.sender import send_message

telegram_celery_app = Celery(
    'telegram_bot',
    broker='amqp://guest:guest@127.0.0.1:5672//',  # Используйте 127.0.0.1 для RabbitMQ
    backend='redis://127.0.0.1:6379/0'             # Используйте 127.0.0.1 для Redis
)


@telegram_celery_app.task
def send_message_via_bot(chat_id, data):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message(chat_id, data))


telegram_celery_app.autodiscover_tasks()

print("***")
print(telegram_celery_app.tasks.keys())
print("***")