import datetime
# import fa as requests
from aiogram import Router, F, types
from aiogram.filters import Filter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import asyncio
from utils.extensions import weekday_name, week_number_from_september, month_name

router = Router()

from aiogram import types


class Search(CallbackData, prefix='my_callback'):
    type: str
    search_id: int
    date: str


@router.callback_query(Search.filter(F.type == "group"))
async def handle_group_callback(callback: types.CallbackQuery, callback_data: Search) -> None:
    # Extract the action and parameters from the callback data
    date = datetime.datetime.fromisoformat(callback_data.date)
    monday_date = date.date() - datetime.timedelta(days=date.weekday())

    group = callback_data.search_id
    action = callback_data.type

    now_date = datetime.datetime.now()
    choosed_week_is_current = week_number_from_september(now_date) == date
    choosed_day_is_current = date == now_date

    response = None

    async with aiohttp.ClientSession() as session:
        print(callback_data.date)
        print(group)
        async with session.get(f'http://api.uksivt.xyz/api/v1/groups/day_schedule/{group}/{callback_data.date}/') as res:
            response = await res.text()
            print(response)

    print(response)
    await callback.message.edit_text(f"🎓 Расписание группы {group}\n"
                                     f"{response}\n"
                                     f"📅 {weekday_name(date)}, {date.day} {month_name(date)}{' - сегодня' if choosed_day_is_current else '' }\n"
                                     f"🏷️ {week_number_from_september(date)} неделя{'- текущая' if choosed_week_is_current else ''}",
         reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
            [
                InlineKeyboardButton(text="ПН", callback_data=Search(type='group',search_id=int(group),date=monday_date.strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="ВТ", callback_data=Search(type='group',search_id=int(group),date=(monday_date+ datetime.timedelta(days=1)).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="СР", callback_data=Search(type='group',search_id=int(group),date=(monday_date+ datetime.timedelta(days=2)).strftime('%Y-%m-%d')).pack()),
            ],
            [
                InlineKeyboardButton(text="ЧТ", callback_data=Search(type='group',search_id=int(group),date=(monday_date+ datetime.timedelta(days=3)).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="ПТ", callback_data=Search(type='group',search_id=int(group),date=(monday_date+ datetime.timedelta(days=4)).strftime('%Y-%m-%d')).pack()),
                InlineKeyboardButton(text="СБ", callback_data=Search(type='group',search_id=int(group),date=(monday_date+ datetime.timedelta(days=5)).strftime('%Y-%m-%d')).pack()),
            ],
            [
                InlineKeyboardButton(text="Пред.неделя⬅️", callback_data=f"group week {group} {monday_date - datetime.timedelta(days=7)}"),
                InlineKeyboardButton(text="Сегодня",callback_data= f'group today {group}'),
                InlineKeyboardButton(text="След.неделя➡️", callback_data=f"group week {group} {monday_date + datetime.timedelta(days=7)}")
            ]]))

    # Acknowledge the callback
    await callback.answer()
