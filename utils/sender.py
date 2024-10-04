import html
from aiogram import Bot
from main import bot


async def send_message(chat_id, message):
    await bot.send_message(chat_id=str(chat_id), text=message)


async def send_error_message(bot: Bot, chat_id: int, error_header: str, application: str,
                             time_: str, error_body: str):
    message = (
        f"<b>⚠️ {error_header}</b>\n"
        f"Application: {application}\n"
        f"Time: {time_}\n\n"
        f"<pre>{html.escape(error_body[:3000])}</pre>"
    )
    await bot.send_message(chat_id=chat_id, text=message, parse_mode='html')
