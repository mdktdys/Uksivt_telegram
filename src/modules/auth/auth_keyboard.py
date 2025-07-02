from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def auth_keyboard(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(keyboard = [[InlineKeyboardButton(text = 'Авторизоваться', callback_data = f'auth_login|{token}')]])