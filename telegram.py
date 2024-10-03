import asyncio

from celery import Celery

from secrets import BROKER_URL, BACKEND_URL
from utils.sender import send_message

telegram_celery_app = Celery(
    'telegram_bot',
    broker=BROKER_URL,
    backend=BACKEND_URL,
)


@telegram_celery_app.task
def send_message_via_bot(chat_id, data):
    loop = asyncio.get_running_loop()
    loop.run_until_complete(send_message(chat_id, data))


telegram_celery_app.autodiscover_tasks(force=True)

print("***")
print(telegram_celery_app.tasks.keys())
print("***")