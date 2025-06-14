from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def change_name_screen():
    return '✍️ Ваше отображаемое имя\n\nвведите новое для изменения'

def change_name_screen_keyboard() -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    keyboard.append([InlineKeyboardButton(text = 'Назад', callback_data = 'settings_screen')])
    return InlineKeyboardMarkup(inline_keyboard = keyboard)