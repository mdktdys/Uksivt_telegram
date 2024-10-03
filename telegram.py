import asyncio
import functools

from celery import Celery

from secrets import BROKER_URL, BACKEND_URL
from utils.sender import send_message

telegram_celery_app = Celery(
    'telegram_bot',
    broker=BROKER_URL,
    backend=BACKEND_URL,
)


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return wrapper


@telegram_celery_app.task
@sync
async def send_message_via_bot(chat_id, data):
    await send_message(chat_id, data)


telegram_celery_app.autodiscover_tasks(force=True)

print("***")
print(telegram_celery_app.tasks.keys())
print("***")