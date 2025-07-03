from models.timings_model import Timings


def timings_screen(timings: list[Timings] | None) -> str:
    text = "🔔 Расписание звонков без обеда\n"
    if not timings:
        return text + "Не удалось получить расписание звонков"

    text += "\n".join([f"{timing.number}  {timing.start.strftime('%H:%M')} — {timing.end.strftime('%H:%M')}" for timing in timings])
    return text


def obed_timings_screen(timings: list[Timings] | None) -> str:
    text = "🍽️ Расписание звонков с обедом\n"
    if not timings:
        return text + "Не удалось получить расписание звонков"

    text += "\n".join([f"{timing.number}  {timing.obed_start.strftime('%H:%M')} — {timing.obed_end.strftime('%H:%M')}" for timing in timings])
    return text

def saturday_timings_screen(timings: list[Timings] | None) -> str:
    text = "📅 Расписание звонков по субботе\n"
    if not timings:
        return text + "Не удалось получить расписание звонков"

    text += "\n".join([f"{timing.number}  {timing.saturday_start.strftime('%H:%M')} — {timing.saturday_end.strftime('%H:%M')}" for timing in timings])
    return text