import datetime

from aiogram.filters.callback_data import CallbackData


class Search(CallbackData, prefix="my_callback"):
    type: str
    search_id: int
    date: str


class Notification(CallbackData, prefix="my_callback"):
    type: str
    search_id: int
    target_type: int
    target_id: int
    is_subscribe: bool
    date: datetime.date
