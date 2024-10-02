import datetime
import pytz
from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.parser import admins

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
    await bot.send_message(chat_id=admins[0], text='🟢 Включен')
    keyboard = create_keyboard_with_logo()
    # res = await bot.edit_message_text(
    #     f"🟢 🌊 uksivt.xyz\nПоиск по группам, преподам и кабинетам\nвключен {get_current_time()}",
    #     chat_id=-1002035415883, message_id=80, reply_markup=keyboard)


async def on_exit(bot: Bot):
    await bot.send_message(chat_id=admins[0], text='💤 Выключен')
    keyboard = create_keyboard_with_logo()
    # res = await bot.edit_message_text(
    #     f"💤 🌊 uksivt.xyz\nПоиск по группам, преподам и кабинетам\nвыключен {get_current_time()}",
    #     chat_id=-1002035415883, reply_markup=keyboard, message_id=80)


async def on_check(bot: Bot):
    await bot.send_message(chat_id=admins[0], text='Проверил')
    keyboard = create_keyboard_with_logo()
    res = await bot.edit_message_text(
        f"🟢 Последняя проверка {get_current_time()}\nuksivt.xyz Поиск по группам, преподам и кабинетам",
        chat_id=-1002035415883, message_id=80, reply_markup=keyboard)