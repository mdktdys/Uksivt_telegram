import datetime

import pytz
from aiogram import Bot, Router
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           WebAppInfo)

from core.enums.log_level_enum import LogLevel
from my_secrets import MAIN_CHANNEL, MAIN_CHANNEL_ANCHOR_MESSAGE
from utils import logger

router = Router()

def create_keyboard_with_logo() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🐋", web_app = WebAppInfo(url = 'https://uksivt.xyz/')
                )
            ]
        ]
    )


def get_current_time():
    tz = pytz.timezone("Asia/Yekaterinburg")
    times: datetime.datetime = datetime.datetime.now(tz=tz)
    return times.strftime("%H:%M %d.%m")


async def on_on(bot: Bot) -> None:
    await logger.log(level = LogLevel.CRITICAL, text = '🟢 Telegram Включен', bot = bot)
    keyboard: InlineKeyboardMarkup = create_keyboard_with_logo()
    try:
        await bot.edit_message_text(
            f"uksivt.xyz\nПоиск по группам и преподам\nвключен {get_current_time()}",
            chat_id=MAIN_CHANNEL,
            message_id=MAIN_CHANNEL_ANCHOR_MESSAGE,
            reply_markup=keyboard,
        )
        pass
    except Exception as e:
        print(e)
        pass


async def on_exit(bot: Bot) -> None:
    await logger.log(level = LogLevel.CRITICAL, text = '💤 Telegram Выключен', bot = bot)
    keyboard: InlineKeyboardMarkup = create_keyboard_with_logo()
    await bot.edit_message_text(
        f"💤 uksivt.xyz\nПоиск по группам и преподам\nвыключен {get_current_time()}",
        chat_id = MAIN_CHANNEL,
        reply_markup = keyboard,
        message_id = MAIN_CHANNEL_ANCHOR_MESSAGE,
    )


async def on_check_start(bot: Bot) -> None:
    await logger.log(level = LogLevel.INFO, text = 'Начал проверку', bot = bot)


async def on_check_end(bot: Bot, result: str) -> None:
    keyboard: InlineKeyboardMarkup = create_keyboard_with_logo()
    
    await logger.log(level = LogLevel.INFO, text = f'Проверил {result}', bot = bot)

    try:
        await bot.edit_message_text(
            f"Проверено {get_current_time()}\nuksivt.xyz Поиск по группам и преподам",
            chat_id=MAIN_CHANNEL,
            message_id=MAIN_CHANNEL_ANCHOR_MESSAGE,
            reply_markup=keyboard,
            parse_mode="html",
        )
    except Exception as e:
        print(e)
        pass
        pass
