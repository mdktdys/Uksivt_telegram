from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def menu_screen_keyboard() -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    keyboard.append([InlineKeyboardButton(text = 'Изменить имя', callback_data = 'change_name')])
    return InlineKeyboardMarkup(inline_keyboard = keyboard)