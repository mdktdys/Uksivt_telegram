from datetime import datetime, timedelta


def weekday_name(date: datetime) -> str:
    days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье",
    ]
    return days[date.weekday()]


def month_name(date: datetime) -> str:
    months = [
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


def get_current_week_number():
    today = datetime.today()

    year = today.year
    start_date = datetime(year, 9, 1)
    end_date = datetime(year + 1, 6, 30)

    if today.month in [7, 8]:
        return None

    if today.month < 9:
        start_date = datetime(year - 1, 9, 1)
        end_date = datetime(year, 6, 30)

    week_number = (today - start_date).days // 7 + 1
    return week_number
