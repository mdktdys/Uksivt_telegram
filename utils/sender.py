import datetime
import html
from aiogram import Bot
from main import bot
from my_secrets import DEBUG_CHANNEL


async def send_message(chat_id, message: str):
    try:
        await bot.send_message(chat_id=str(chat_id), text=str(message))
    except Exception as e:
        await send_error_message(
            bot=bot,
            chat_id=DEBUG_CHANNEL,
            error_header=f"Ошибка\nchat_id:{chat_id}\nmessage:{message}",
            application="Kronos",
            time_=str(datetime.datetime.now()),
            error_body=str(e),
        )

async def send_multicast_message(chat_ids: list[str], message: str):
    try:
        for chat in chat_ids:
            await bot.send_message(
                chat_id = chat,
                text = message
            )
    except Exception as e:
        print(e)
        await send_error_message(
            bot=bot,
            chat_id=DEBUG_CHANNEL,
            error_header = "Ошибка отправки уведомлений в чатах",
            application = "Kronos",
            time_=str(datetime.datetime.now()),
            error_body=str(e),
        )

async def send_error_message(
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
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="html")
