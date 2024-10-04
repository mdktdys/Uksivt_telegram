import datetime
import html
import traceback
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from secrets import DEBUG_CHANNEL

router = Router()

admins = [1283168392]


@router.message(F.text, Command("latest"))
async def my_handler(message: Message):
    try:
        chat_id = message.chat.id
        # Lazy import inside the function
        from telegram_celery import telegram_celery_app
        telegram_celery_app.send_task("parser.tasks.get_latest_zamena_link_telegram",args=[chat_id])
    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message
        await send_error_message(
            bot=message.bot,
            chat_id=DEBUG_CHANNEL,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )


@router.message(F.text, Command("check"))
async def my_handler(message: Message):
    try:
        # Lazy import inside the function
        from telegram_celery import telegram_celery_app
        telegram_celery_app.send_task("parser.tasks.check_new",args=[])
    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message
        await send_error_message(
            bot=message.bot,
            chat_id=DEBUG_CHANNEL,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )