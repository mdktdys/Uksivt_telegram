from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.settings_keyboard import settings_screen, settings_screen_keyboard

router = Router(name = 'settings_router')


@router.callback_query(F.data == "settings_screen")
async def show_settings(callback: CallbackQuery) -> None:
    text = settings_screen()
    callback.bot.send_message(text = text, reply_markup = settings_screen_keyboard())
    pass