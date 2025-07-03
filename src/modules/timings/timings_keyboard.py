from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def timings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text='🔄 Обновить', callback_data='timings_screen')],
        [InlineKeyboardButton(text='🍖 Без обеда', callback_data='obed_timings_screen')],
        [InlineKeyboardButton(text='⛵ По субботе', callback_data='saturday_timings_screen')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='menu_screen')]
    ])
    

def obed_timings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text='🔄 Обновить', callback_data='obed_timings_screen')],
        [InlineKeyboardButton(text='🥗 С обедом', callback_data='timings_screen')],
        [InlineKeyboardButton(text='⛵ По субботе', callback_data='saturday_timings_screen')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='menu_screen')]
    ])
    

def saturday_timings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text='🔄 Обновить', callback_data='saturday_timings_screen')],
        [InlineKeyboardButton(text='📅 Обычное', callback_data='timings_screen')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='menu_screen')]
    ])