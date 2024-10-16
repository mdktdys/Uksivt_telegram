import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.search_result_callback import Search


def build_keyboard(
    monday_date: datetime.date,
    week_day: int,
    search_id: int,
    search_type: str,
    date: datetime.date,
):
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]

    day_buttons = [
        InlineKeyboardButton(
            text=day + (" 🟢" if week_day == idx else ""),
            callback_data=Search(
                type=search_type,
                search_id=search_id,
                date=(monday_date + datetime.timedelta(days=idx)).strftime("%Y-%m-%d"),
            ).pack(),
        )
        for idx, day in enumerate(days)
    ]

    day_buttons_rows = [day_buttons[i : i + 3] for i in range(0, len(day_buttons), 3)]

    navigation_buttons = [
        InlineKeyboardButton(
            text="Пред.неделя⬅️",
            callback_data=Search(
                type=search_type,
                search_id=search_id,
                date=(date - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Сегодня",
            callback_data=Search(
                type=search_type,
                search_id=search_id,
                date=datetime.datetime.now().strftime("%Y-%m-%d"),
            ).pack(),
        ),
        InlineKeyboardButton(
            text="След.неделя➡️",
            callback_data=Search(
                type=search_type,
                search_id=search_id,
                date=(date + datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=day_buttons_rows + [navigation_buttons])
