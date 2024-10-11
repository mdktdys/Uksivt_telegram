import datetime
import traceback

from aiogram import Bot

from callbacks.events import on_check_start
from secrets import DEBUG_CHANNEL


async def check_new_zamena(bot: Bot):
    try:
        await on_check_start(bot=bot)
    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message

        await send_error_message(
            bot=bot,
            chat_id=DEBUG_CHANNEL,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )
