import datetime
import html

import pytz
from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# from callbacks.parser import admins
from my_secrets import MAIN_CHANNEL, MAIN_CHANNEL_ANCHOR_MESSAGE, DEBUG_CHANNEL

router = Router()


def create_keyboard_with_logo():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🐋", url="https://t.me/UksivtZameny_bot/zameny_uksivt/"
                )
            ]
        ]
    )


def get_current_time():
    tz = pytz.timezone("Asia/Yekaterinburg")
    times = datetime.datetime.now(tz=tz)
    return times.strftime("%H:%M %d.%m")


async def on_on(bot: Bot):
    await bot.send_message(chat_id=DEBUG_CHANNEL, text="🟢 Telegram Включен")
    keyboard = create_keyboard_with_logo()
    try:
        await bot.edit_message_text(
            f"uksivt.xyz\nПоиск по группам, преподам и кабинетам\nвключен {get_current_time()}",
            chat_id=MAIN_CHANNEL,
            message_id=MAIN_CHANNEL_ANCHOR_MESSAGE,
            reply_markup=keyboard,
        )
        pass
    except Exception as e:
        print(e)
        pass


async def on_exit(bot: Bot):
    await bot.send_message(chat_id=DEBUG_CHANNEL, text="💤 Telegram Выключен")
    keyboard = create_keyboard_with_logo()
    await bot.edit_message_text(
        f"💤 uksivt.xyz\nПоиск по группам, преподам и кабинетам\nвыключен {get_current_time()}",
        chat_id=MAIN_CHANNEL,
        reply_markup=keyboard,
        message_id=MAIN_CHANNEL_ANCHOR_MESSAGE,
    )


async def on_check_start(bot: Bot):
    await bot.send_message(chat_id=DEBUG_CHANNEL, text="Начал проверку")


async def on_check_end(bot: Bot, result: str) -> None:
    keyboard = create_keyboard_with_logo()

    await bot.send_message(
        chat_id=DEBUG_CHANNEL,
        text=f"Проверил {result}",
        parse_mode="html",
    )

    try:
        await bot.edit_message_text(
            f"❄️ Проверено {get_current_time()}\nuksivt.xyz Поиск по группам, преподам и кабинетам",
            chat_id=MAIN_CHANNEL,
            message_id=MAIN_CHANNEL_ANCHOR_MESSAGE,
            reply_markup=keyboard,
            parse_mode="html",
        )
    except Exception as e:
        print(e)
        pass
