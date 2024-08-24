import datetime


def weekday_name(date: datetime.datetime) -> str:
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return days[date.weekday()]


def month_name(date: datetime.datetime) -> str:
    months = [
        'январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
        'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'
    ]
    return months[date.month - 1]


def week_number_from_september(date: datetime.datetime) -> int:
    first_september = datetime.date(2024, 9, 1)
    if date.date() < first_september:
        return 0
    days_difference = (date - first_september).days
    week_number = days_difference // 7 + 1
    return week_number
