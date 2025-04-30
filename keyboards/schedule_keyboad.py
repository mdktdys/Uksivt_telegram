import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.search_result_callback import Search, Notification


def build_keyboard(
    monday_date: datetime.date,
    week_day: int,
    search_id: int,
    search_type: str,
    date: datetime.date,
    is_subscribed: bool,
) -> None | InlineKeyboardMarkup:

    target_type_id: int = 1
    if search_type != "teacher" and search_type != "group":
        return
    if search_type == "teacher":
        target_type_id = 2
    if search_type == "group":
        target_type_id = 1

    notification_buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text="🔔" if is_subscribed else "🔕",
            callback_data=Notification(
                date=date.strftime("%Y-%m-%d"),
                search_id=search_id,
                type=search_type,
                target_type=target_type_id,
                target_id=search_id,
                is_subscribe=is_subscribed,
            ).pack(),
        )
    ]

    days: list[str] = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]

    day_buttons: list[InlineKeyboardButton] = [
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

    day_buttons_rows: list[list[InlineKeyboardButton]] = [day_buttons[i : i + 3] for i in range(0, len(day_buttons), 3)]

    navigation_buttons: list[InlineKeyboardButton] = [
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

    return InlineKeyboardMarkup(
        inline_keyboard=[notification_buttons] + day_buttons_rows + [navigation_buttons]
    )
