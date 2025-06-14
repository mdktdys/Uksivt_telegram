from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def settings_screen():
    return '⚙️ Настройки'

def settings_screen_keyboard() -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    
    keyboard.append([InlineKeyboardButton(text = 'Изменить имя', callback_data = 'change_name_screen')])
    keyboard.append([InlineKeyboardButton(text = 'Назад', callback_data = 'menu_screen')])
    return InlineKeyboardMarkup(inline_keyboard = keyboard)

1
3
7
8
12
15
28