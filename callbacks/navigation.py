import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import aiohttp
from aiogram import types

from secrets import API_URL
from models.search_result import DayScheduleFormatted
from utils.extensions import weekday_name, week_number_from_september, month_name
router = Router()


class Search(CallbackData, prefix='my_callback'):
    type: str
    search_id: int
    date: str


@router.callback_query(Search.filter(F.type == "group"))
async def handle_group_callback(callback: types.CallbackQuery, callback_data: Search) -> None:

    date = datetime.datetime.fromisoformat(callback_data.date)
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    group = callback_data.search_id
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september(now_date) == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(f'{API_URL}groups/day_schedule_formatted/{group}/{callback_data.date}/')
        async with session.get(f'{API_URL}groups/day_schedule_formatted/{group}/{callback_data.date}/') as res:
            debug = res.headers['x-fastapi-cache']
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(await res.text())


    header = f"🎓 Расписание группы {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else '\n🎉 Нет пар'
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else '' }"
    await callback.message.edit_text(
                                     f"{header}"
                                     f"{body}"
                                     f"\n{calendar_footer}"
                                     f"\n🏷️ {week_number_from_september(date)} Неделя {'- текущая' if choosed_week_is_current else ''}"
                                     f"{debug}",
         reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
            [
                InlineKeyboardButton(text="ПН"+(" 🟢" if week_day == 0 else ""), callback_data=Search(type='group',search_id=int(group),date=monday_date.strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="ВТ"+(" 🟢" if week_day == 1 else ""), callback_data=Search(type='group',search_id=int(group),date=(monday_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="СР"+(" 🟢" if week_day == 2 else ""), callback_data=Search(type='group',search_id=int(group),date=(monday_date + datetime.timedelta(days=2)).strftime('%Y-%m-%d')).pack()),
            ],
            [
                InlineKeyboardButton(text="ЧТ"+(" 🟢" if week_day == 3 else ""), callback_data=Search(type='group',search_id=int(group),date=(monday_date + datetime.timedelta(days=3)).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="ПТ"+(" 🟢" if week_day == 4 else ""), callback_data=Search(type='group',search_id=int(group),date=(monday_date + datetime.timedelta(days=4)).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="СБ"+(" 🟢" if week_day == 5 else ""), callback_data=Search(type='group',search_id=int(group),date=(monday_date + datetime.timedelta(days=5)).strftime('%Y-%m-%d')).pack()),
            ],
            [
                InlineKeyboardButton(text="Пред.неделя⬅️", callback_data=Search(type='group',search_id=int(group),date=(date - datetime.timedelta(days=7)).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="Сегодня",callback_data=Search(type='group',search_id=int(group),date=(datetime.datetime.now()).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="След.неделя➡️", callback_data=Search(type='group',search_id=int(group),date=(date + datetime.timedelta(days=7)).strftime('%Y-%m-%d')).pack())
            ]]))

    await callback.answer()


@router.message(Command('group'))
async def a(message: Message) -> None:
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    group = message.text.split(' ')[1]
    date: datetime.datetime = datetime.datetime.fromtimestamp(float(message.text.split(' ')[2]))
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september(now_date) == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(f'{API_URL}groups/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/')
        async with session.get(
                f'{API_URL}groups/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/') as res:
            debug = res.headers['x-fastapi-cache']
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(await res.text())

    header = f"🎓 Расписание группы {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else '\n🎉 Нет пар'
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else ''}"

    await message.answer(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number_from_september(date)} Неделя {'- текущая' if choosed_week_is_current else ''}"
        f"{debug}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="ПН" + (" 🟢" if week_day == 0 else ""),
                                         callback_data=Search(type='group', search_id=int(group),
                                                              date=monday_date.strftime('%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="ВТ" + (" 🟢" if week_day == 1 else ""),
                                         callback_data=Search(type='group', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(days=1)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="СР" + (" 🟢" if week_day == 2 else ""),
                                         callback_data=Search(type='group', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(days=2)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                ],
                [
                    InlineKeyboardButton(text="ЧТ" + (" 🟢" if week_day == 3 else ""),
                                         callback_data=Search(type='group', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(days=3)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="ПТ" + (" 🟢" if week_day == 4 else ""),
                                         callback_data=Search(type='group', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(days=4)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="СБ" + (" 🟢" if week_day == 5 else ""),
                                         callback_data=Search(type='group', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(days=5)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                ],
                [
                    InlineKeyboardButton(text="Пред.неделя⬅️", callback_data=Search(type='group', search_id=int(group),
                                                                                    date=(date - datetime.timedelta(
                                                                                        days=7)).strftime(
                                                                                        '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="Сегодня", callback_data=Search(type='group', search_id=int(group),
                                                                              date=(datetime.datetime.now()).strftime(
                                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="След.неделя➡️", callback_data=Search(type='group', search_id=int(group),
                                                                                    date=(date + datetime.timedelta(
                                                                                        days=7)).strftime(
                                                                                        '%Y-%m-%d')).pack())
                ]]), )


@router.callback_query(Search.filter(F.type == "teacher"))
async def handle_group_callback(callback: types.CallbackQuery, callback_data: Search) -> None:
    date = datetime.datetime.fromisoformat(callback_data.date)
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    group = callback_data.search_id
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september(now_date) == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(f'{API_URL}teachers/day_schedule_formatted/{group}/{callback_data.date}/')
        async with session.get(
                f'{API_URL}teachers/day_schedule_formatted/{group}/{callback_data.date}/') as res:
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(await res.text())

    header = f"🎓 Расписание преподавателя {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else '\n🎉 Нет пар'
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else ''}"

    await callback.message.edit_text(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number_from_september(date)} Неделя {'- текущая' if choosed_week_is_current else ''}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="ПН" + (" 🟢" if week_day == 0 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=monday_date.strftime('%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="ВТ" + (" 🟢" if week_day == 1 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group), date=(
                                                     monday_date + datetime.timedelta(days=1)).strftime(
                                             '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="СР" + (" 🟢" if week_day == 2 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group), date=(
                                                     monday_date + datetime.timedelta(days=2)).strftime(
                                             '%Y-%m-%d')).pack()),
                ],
                [
                    InlineKeyboardButton(text="ЧТ" + (" 🟢" if week_day == 3 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group), date=(
                                                     monday_date + datetime.timedelta(days=3)).strftime(
                                             '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="ПТ" + (" 🟢" if week_day == 4 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group), date=(
                                                     monday_date + datetime.timedelta(days=4)).strftime(
                                             '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="СБ" + (" 🟢" if week_day == 5 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group), date=(
                                                     monday_date + datetime.timedelta(days=5)).strftime(
                                             '%Y-%m-%d')).pack()),
                ],
                [
                    InlineKeyboardButton(text="Пред.неделя⬅️",
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(date - datetime.timedelta(days=7)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="Сегодня", callback_data=Search(type='teacher', search_id=int(group),
                                                                              date=(
                                                                                  datetime.datetime.now()).strftime(
                                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="След.неделя➡️",
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(date + datetime.timedelta(days=7)).strftime(
                                                                  '%Y-%m-%d')).pack())
                ]]))

    await callback.answer()


@router.message(Command('teacher'))
async def a(message: Message) -> None:
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    group = message.text.split(' ')[1]
    date: datetime.datetime = datetime.datetime.fromtimestamp(float(message.text.split(' ')[2]))
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september(now_date) == date
    choosed_day_is_current = True if date == now_date else False
    week_day = date.weekday()

    async with aiohttp.ClientSession(trust_env=True) as session:
        print(f'{API_URL}teachers/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/')
        async with session.get(
                f'{API_URL}teachers/day_schedule_formatted/{group}/{datetime.datetime.now().strftime("%Y-%m-%d")}/') as res:
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(await res.text())

    header = f"🎓 Расписание преподавателя {response.search_name}\n"
    body = "\n".join(response.paras) if response.paras else '\n🎉 Нет пар'
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else ''}"

    await message.answer(
        f"{header}"
        f"{body}"
        f"\n{calendar_footer}"
        f"\n🏷️ {week_number_from_september(date)} Неделя {'- текущая' if choosed_week_is_current else ''}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="ПН" + (" 🟢" if week_day == 0 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=monday_date.strftime('%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="ВТ" + (" 🟢" if week_day == 1 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(
                                                                  days=1)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="СР" + (" 🟢" if week_day == 2 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(
                                                                  days=2)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                ],
                [
                    InlineKeyboardButton(text="ЧТ" + (" 🟢" if week_day == 3 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(
                                                                  days=3)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="ПТ" + (" 🟢" if week_day == 4 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(
                                                                  days=4)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="СБ" + (" 🟢" if week_day == 5 else ""),
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(monday_date + datetime.timedelta(
                                                                  days=5)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                ],
                [
                    InlineKeyboardButton(text="Пред.неделя⬅️",
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(date - datetime.timedelta(
                                                                  days=7)).strftime(
                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="Сегодня", callback_data=Search(type='teacher', search_id=int(group),
                                                                              date=(
                                                                                  datetime.datetime.now()).strftime(
                                                                                  '%Y-%m-%d')).pack()),
                    InlineKeyboardButton(text="След.неделя➡️",
                                         callback_data=Search(type='teacher', search_id=int(group),
                                                              date=(date + datetime.timedelta(
                                                                  days=7)).strftime(
                                                                  '%Y-%m-%d')).pack())
                ]]), )