import datetime
import pytz
from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.parser import admins
from secrets import MAIN_CHANNEL, MAIN_CHANNEL_ANCHOR_MESSAGE, DEBUG_CHANNEL

router = Router()


def create_keyboard_with_logo():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🐋", url="https://uksivt.xyz/")]]
    )


def get_current_time():
    tz = pytz.timezone('Asia/Yekaterinburg')
    times = datetime.datetime.now(tz=tz)
    return times.strftime("%H:%M %d.%m")


async def on_on(bot: Bot):
    await bot.send_message(chat_id=DEBUG_CHANNEL, text='🟢 Telegram Включен')
    keyboard = create_keyboard_with_logo()
    res = await bot.edit_message_text(
        f"🟢 🌊 uksivt.xyz\nПоиск по группам, преподам и кабинетам\nвключен {get_current_time()}",
        chat_id=MAIN_CHANNEL, message_id=MAIN_CHANNEL_ANCHOR_MESSAGE, reply_markup=keyboard)


async def on_exit(bot: Bot):
    await bot.send_message(chat_id=DEBUG_CHANNEL, text='💤 Telegram Выключен')
    keyboard = create_keyboard_with_logo()
    res = await bot.edit_message_text(
        f"💤 🌊 uksivt.xyz\nПоиск по группам, преподам и кабинетам\nвыключен {get_current_time()}",
        chat_id=MAIN_CHANNEL, reply_markup=keyboard, message_id=MAIN_CHANNEL_ANCHOR_MESSAGE)


async def on_check(bot: Bot):
    await bot.send_message(chat_id=DEBUG_CHANNEL, text='Проверил')
    keyboard = create_keyboard_with_logo()
    res = await bot.edit_message_text(
        f"🟢 Последняя проверка {get_current_time()}\nuksivt.xyz Поиск по группам, преподам и кабинетам",
        chat_id=MAIN_CHANNEL, message_id=MAIN_CHANNEL_ANCHOR_MESSAGE, reply_markup=keyboard)