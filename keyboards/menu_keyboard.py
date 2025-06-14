from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def menu_screen():
    return 'Для поиска расписания в чатах начните вводить (Бот должен состоять в чате)\n@UksivtZameny_bot [Наименование]'

def menu_screen_keyboard() -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    
    keyboard.append([InlineKeyboardButton(text='Поиск', switch_inline_query_current_chat = '')])
    keyboard.append([
        InlineKeyboardButton(text="🐋", url="https://uksivt.xyz/"),
        InlineKeyboardButton(text = 'Изменить имя', callback_data = 'change_name'),
    ])
    return InlineKeyboardMarkup(inline_keyboard = keyboard)