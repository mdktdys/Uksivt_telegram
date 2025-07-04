from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def auth_keyboard(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = 'Авторизоваться', callback_data = f'auth_login|{token}')]])


def auth_success_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = '🗑️ Удалить сообщение', callback_data = 'delete_message')]])