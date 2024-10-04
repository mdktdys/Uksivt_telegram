import datetime
import html
from aiogram import Bot
from main import bot, dp
from secrets import DEBUG_CHANNEL


def send_message(chat_id, message: str):
    try:
        dp.loop.run_until_complete(
            bot.send_message(chat_id=str(chat_id), text=str(message))
        )
    except Exception as e:
        send_error_message(
            bot=bot,
            chat_id=DEBUG_CHANNEL,
            error_header=f"Ошибка\nchat_id:{chat_id}\nmessage:{message}",
            application="Kronos",
            time_=str(datetime.datetime.now()),
            error_body=str(e),
        )


def send_error_message(
    bot: Bot,
    chat_id: int,
    error_header: str,
    application: str,
    time_: str,
    error_body: str,
):
    message = (
        f"<b>⚠️ {error_header}</b>\n"
        f"Application: {application}\n"
        f"Time: {time_}\n\n"
        f"<pre>{html.escape(error_body[:3000])}</pre>"
    )
    dp.loop.run_until_complete(
        bot.send_message(chat_id=chat_id, text=message, parse_mode="html")
    )
