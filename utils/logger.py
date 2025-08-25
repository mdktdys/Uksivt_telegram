import datetime
import html
from logging import DEBUG, Logger, StreamHandler, getLogger
from typing import TextIO

from aiogram import Bot
from pyfiglet import Figlet

from core.enums.log_level_enum import LogLevel
from my_secrets import DEBUG_CHANNEL

logger: Logger = getLogger()
logger.setLevel(DEBUG)
handler: StreamHandler[TextIO] = StreamHandler()
handler.setLevel(DEBUG)
logger.addHandler(handler)

print(Figlet(font = 'doom').renderText('DEV @MDKTDYS'))

async def log(level: LogLevel, text: str, bot: Bot):
    message = ''
    if level == LogLevel.CRITICAL:
        message: str = (
            f"<b>⚠️ Критикал</b>\n"
            f"Time: {datetime.datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}\n\n"
            f"<pre>{html.escape(text[:3000])}</pre>"
        )

    if level == LogLevel.DEBUG:
        message: str = (
            f"<b>Дебаг</b>\n"
            f"Time: {datetime.datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}\n\n"
            f"<pre>{html.escape(text[:3000])}</pre>"
        )
        
    if level == LogLevel.INFO:
        message: str = (
            f"<b>Инфо</b>\n"
            f"Time: {datetime.datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}\n\n"
            f"<pre>{html.escape(text[:3000])}</pre>"
        )
        
    await bot.send_message(
        chat_id = DEBUG_CHANNEL,
        parse_mode = "html",
        text = message,
    )
    
    





