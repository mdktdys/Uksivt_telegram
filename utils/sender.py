import datetime
import html
from aiogram import Bot
from main import bot
from my_secrets import DEBUG_CHANNEL


async def send_message(
    chat_id,
    message: str
) -> None:
    try:
        await bot.send_message(
            chat_id=str(chat_id),
            text=str(message)
        )
    except Exception as e:
        await send_error_message(
            error_header = f"Ошибка\nchat_id:{chat_id}\nmessage:{message}",
            time_=str(datetime.datetime.now()),
            chat_id = DEBUG_CHANNEL,
            application = "Kronos",
            error_body=str(e),
            bot = bot,
        )


async def send_error_message(
    chat_id: int | str,
    error_header: str,
    application: str,
    error_body: str,
    time_: str,
    bot: Bot,
) -> None:
    message: str = (
        f"<b>⚠️ {error_header}</b>\n"
        f"Application: {application}\n"
        f"Time: {time_}\n\n"
        f"<pre>{html.escape(error_body[:3000])}</pre>"
    )
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="html") 
