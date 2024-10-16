from aiogram.filters.callback_data import CallbackData


class Search(CallbackData, prefix="my_callback"):
    type: str
    search_id: int
    date: str
