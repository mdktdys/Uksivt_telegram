import asyncio
import functools
from telegram_celery import telegram_celery_app
from utils.sender import send_message
import celery_pool_asyncio


# def sync(f):
#     @functools.wraps(f)
#     def wrapper(*args, **kwargs):
#         return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
#
#     return wrapper


@telegram_celery_app.task
async def send_message_via_bot(chat_id, data):
    await send_message(chat_id, data)
