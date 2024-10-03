import datetime
import html
import traceback
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

admins = [1283168392]


@router.message(F.text, Command("latest"))
async def my_handler(message: Message):
    try:
        chat_id = message.chat.id
        # Lazy import inside the function
        from telegram import telegram_celery_app
        res = await telegram_celery_app.send_task("parser.tasks.get_latest_zamena_link")
        await message.answer(f"{res}")
    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message
        await send_error_message(
            bot=message.bot,
            chat_id=message.chat.id,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )

