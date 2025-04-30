import datetime


def weekday_name(date: datetime.date) -> str:
    days: list[str] = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье",
    ]
    return days[date.weekday()]


def month_name(date: datetime.date) -> str:
    months: list[str] = [
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ]
    return months[date.month - 1]


def week_number_from_september() -> None | int:
    today: datetime.date = datetime.date.today()

    year: int = today.year
    start_date = datetime.date(year, 9, 1)
    end_date = datetime.date(year + 1, 6, 30)

    if today.month in [7, 8]:
        return None

    if today.month < 9:
        start_date = datetime.date(year - 1, 9, 1)
        end_date = datetime.date(year, 6, 30)

    week_number = (today - start_date).days // 7 + 1
    return week_number
