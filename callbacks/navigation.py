import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
from aiogram import types

from keyboards.schedule_keyboad import build_keyboard
from models.search_result_callback import Search, Notification
from my_secrets import API_URL, API_KEY
from models.search_result import DayScheduleFormatted
from utils.extensions import weekday_name, month_name, week_number_from_september

router = Router()


@router.callback_query(Notification.filter(F.type == "group"))
async def handle_notification_callback(
    callback: types.CallbackQuery, callback_data: Notification
) -> None:
    date = datetime.datetime.fromisoformat(callback_data.date)
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    group = callback_data.search_id
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september() == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(f"{API_URL}groups/day_schedule_formatted/{group}/{callback_data.date}/")
        async with session.get(
            f"{API_URL}groups/day_schedule_formatted/{group}/{callback_data.date}/",
            headers={"X-API-KEY": API_KEY},
        ) as res:
            debug = res.headers["x-fastapi-cache"]
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(
                await res.text()
            )

    header = f"🎓 Расписание группы {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else "\n🎉 Нет пар"
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else '' }"
    week_number = week_number_from_september()
    await callback.message.edit_text(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number} Неделя {'- текущая' if choosed_week_is_current else ''}"
        f"{debug}",
        reply_markup=build_keyboard(
            date=date,
            monday_date=monday_date,
            search_id=int(group),
            week_day=week_day,
            search_type="group",
            is_subscribed=False,
        ),
    )

    await callback.answer()


@router.callback_query(Search.filter(F.type == "group"))
async def handle_group_callback(
    callback: types.CallbackQuery, callback_data: Search
) -> None:

    date = datetime.datetime.fromisoformat(callback_data.date)
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    group = callback_data.search_id
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september() == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(f"{API_URL}groups/day_schedule_formatted/{group}/{callback_data.date}/")
        async with session.get(
            f"{API_URL}groups/day_schedule_formatted/{group}/{callback_data.date}/",
            headers={"X-API-KEY": API_KEY},
        ) as res:
            debug = res.headers["x-fastapi-cache"]
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(
                await res.text()
            )

    header = f"🎓 Расписание группы {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else "\n🎉 Нет пар"
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else '' }"
    week_number = week_number_from_september()
    await callback.message.edit_text(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number} Неделя {'- текущая' if choosed_week_is_current else ''}"
        f"{debug}",
        reply_markup=build_keyboard(
            date=date,
            monday_date=monday_date,
            search_id=int(group),
            week_day=week_day,
            search_type="group",
            is_subscribed=False,
        ),
    )

    await callback.answer()


@router.message(Command("group"))
async def a(message: Message) -> None:
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id
        )
    except:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text="Я не могу удалять сообщения за собой(\nВыдайте полную админку пж((",
        )
    group = message.text.split(" ")[1]
    date: datetime.datetime = datetime.datetime.fromtimestamp(
        float(message.text.split(" ")[2])
    )
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september() == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(
            f'{API_URL}groups/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/'
        )
        async with session.get(
            f'{API_URL}groups/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/',
            headers={"X-API-KEY": API_KEY},
        ) as res:
            debug = res.headers["x-fastapi-cache"]
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(
                await res.text()
            )

    header = f"🎓 Расписание группы {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else "\n🎉 Нет пар"
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else ''}"
    week_number = week_number_from_september()
    await message.answer(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number} Неделя {'- текущая' if choosed_week_is_current else ''}"
        f"{debug}",
        reply_markup=build_keyboard(
            date=date,
            monday_date=monday_date,
            search_id=int(group),
            week_day=week_day,
            search_type="group",
            is_subscribed=False,
        ),
    )


@router.callback_query(Search.filter(F.type == "teacher"))
async def handle_group_callback(
    callback: types.CallbackQuery, callback_data: Search
) -> None:
    date = datetime.datetime.fromisoformat(callback_data.date)
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    group = callback_data.search_id
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september() == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(f"{API_URL}teachers/day_schedule_formatted/{group}/{callback_data.date}/")
        async with session.get(
            f"{API_URL}teachers/day_schedule_formatted/{group}/{callback_data.date}/",
            headers={"X-API-KEY": API_KEY},
        ) as res:
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(
                await res.text()
            )

    header = f"🎓 Расписание преподавателя {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else "\n🎉 Нет пар"
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else ''}"

    await callback.message.edit_text(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number_from_september()} Неделя {'- текущая' if choosed_week_is_current else ''}",
        reply_markup=build_keyboard(
            date=date,
            monday_date=monday_date,
            search_id=int(group),
            week_day=week_day,
            search_type="teacher",
            is_subscribed=False,
        ),
    )
    await callback.answer()


@router.message(Command("teacher"))
async def a(message: Message) -> None:
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id
        )
    except:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text="Я не могу удалять сообщения за собой(\nВыдайте полную админку пж((",
        )
    group = message.text.split(" ")[1]
    date: datetime.datetime = datetime.datetime.fromtimestamp(
        float(message.text.split(" ")[2])
    )
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september() == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(
            f'{API_URL}teachers/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/'
        )
        async with session.get(
            f'{API_URL}teachers/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/',
            headers={"X-API-KEY": API_KEY},
        ) as res:
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(
                await res.text()
            )

    header = f"🎓 Расписание преподавателя {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else "\n🎉 Нет пар"
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else ''}"

    await message.answer(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number_from_september()} Неделя {'- текущая' if choosed_week_is_current else ''}",
        reply_markup=build_keyboard(
            date=date,
            monday_date=monday_date,
            search_id=int(group),
            week_day=week_day,
            search_type="teacher",
            is_subscribed=False,
        ),
    )
