from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def menu_screen():
    return 'Для поиска расписания в чатах начните вводить (Бот должен состоять в чате)\n@UksivtZameny_bot [Наименование]'

def menu_screen_keyboard() -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    
    keyboard.append([InlineKeyboardButton(text='🔎 Поиск', switch_inline_query_current_chat = '')])
    keyboard.append([
        InlineKeyboardButton(text="🌐 Сайт", url="https://uksivt.xyz/"),
        InlineKeyboardButton(text="🐋 Канал замен", url="https://t.me/bot_uksivt"),
    ])
    keyboard.append([InlineKeyboardButton(text = '⚙️ Настройки', callback_data = 'settings_screen')])
    return InlineKeyboardMarkup(inline_keyboard = keyboard)