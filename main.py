import asyncio
import datetime
import logging
import sys

import requests as req
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity

from callbacks import navigation
from callbacks.navigation import Search
from models import Group

TOKEN = "7283968288:AAEdrChiKr149d2p5zeoVZ29bWEJIFlDtTs"
API_URL = "https://api.uksivt.xyz/api/v1/"

router = Router()


@router.inline_query()
async def handle(query: InlineQuery):
    filter_text = query.query
    if filter_text == '' or filter_text is None:
        return query.answer([InlineQueryResultArticle(
            id=str(-1),
            title="Замены уксивтика",
            description="Добавь текст для поиска",
            url='uksivt.xyz',
            thumbnail_url='https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/00020_3223582996_Cyber_Whale__blue__gradient_background._4k._realistic._Technologt__cyberpunk._photo_realistic__Neomorphism._Beatiful_whale_arrow.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzLzAwMDIwXzMyMjM1ODI5OTZfQ3liZXJfV2hhbGVfX2JsdWVfX2dyYWRpZW50X2JhY2tncm91bmQuXzRrLl9yZWFsaXN0aWMuX1RlY2hub2xvZ3RfX2N5YmVycHVuay5fcGhvdG9fcmVhbGlzdGljX19OZW9tb3JwaGlzbS5fQmVhdGlmdWxfd2hhbGVfYXJyb3cuanBnIiwiaWF0IjoxNzIwMzg5NDc3LCJleHAiOjE3NTE5MjU0Nzd9.OVlPHGRQT0cKQHoIf2q5W7BHUmIbGeMO5k1kyUoIntc&t=2024-07-07T21%3A57%3A56.837Z',
            input_message_content=InputTextMessageContent(message_text='uksivt.xyz', )
        )], cache_time=1, is_personal=True)
    res: list[dict] = req.get(f"{API_URL}search/search/{filter_text}").json()
    print(res)
    if len(res) == 0:
        return query.answer([InlineQueryResultArticle(
            id=str(-1),
            title="Нет результатов",
            description="Попробуй что-то другое",
            url='uksivt.xyz',

            thumbnail_url='https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/Group%201573.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL0dyb3VwIDE1NzMucG5nIiwiaWF0IjoxNzI0Mzk1MjQ4LCJleHAiOjIwMzk3NTUyNDh9.LQH1lSml7HUaWSrkRnxxxS8DJMiRvQJEHp_ErZZLsRE&t=2024-08-23T06%3A40%3A47.304Z',
            input_message_content=InputTextMessageContent(message_text='что я выбрал', )
        )], cache_time=1, is_personal=True)
    if len(res) > 50:
        return query.answer([InlineQueryResultArticle(
            id=str(-1),
            title="Слишком много результатов",
            description="Уточни конкретнее",
            url='uksivt.xyz',
            thumbnail_url='https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/python_(1).png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL3B5dGhvbl8oMSkucG5nIiwiaWF0IjoxNzIwMzg2MDg0LCJleHAiOjE3NTE5MjIwODR9.Xn_fkGftIEKCGFwQRK8JY0HPNnJax6uU8RtxmDUD0A0&t=2024-07-07T21%3A01%3A23.755Z',
            input_message_content=InputTextMessageContent(message_text='что я выбрал', )
        )], cache_time=1, is_personal=True)
    groups: list[Group] = [Group(**group) for group in res]
    results = []
    for group in groups:
        results.append(
            InlineQueryResultArticle(
                id=str(group.id),
                title=group.name,
                url='uksivt.xyz',
                input_message_content=InputTextMessageContent(
                    message_text=f"/group {group.id} {datetime.datetime.now().timestamp()}",
                ),
                # reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                #     [
                #         InlineKeyboardButton(text="ПН", callback_data='monday'),
                #         InlineKeyboardButton(text="ВТ", callback_data='tuesday'),
                #         InlineKeyboardButton(text="СР", callback_data='wednesday')
                #     ],
                #     [
                #         InlineKeyboardButton(text="ЧТ", callback_data='thursday'),
                #         InlineKeyboardButton(text="ПТ", callback_data='friday'),
                #         InlineKeyboardButton(text="СБ", url="https://www.gooadsgle.com/", callback_data='saturday')
                #     ],
                #     [
                #         InlineKeyboardButton(text="Пред.неделя⬅️", url="https://www.gooasdgle.com/"),
                #         InlineKeyboardButton(text="Сегодня", url="https://www.goadsgle.com/"),
                #         InlineKeyboardButton(text="След.неделя➡️", url="https://www.gooadsgle.com/")
                #     ]
                # ]),
                thumbnail_url='https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/python_(1).png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL3B5dGhvbl8oMSkucG5nIiwiaWF0IjoxNzIwMzg2MDg0LCJleHAiOjE3NTE5MjIwODR9.Xn_fkGftIEKCGFwQRK8JY0HPNnJax6uU8RtxmDUD0A0&t=2024-07-07T21%3A01%3A23.755Z',
            )
        )
    await query.answer(results, cache_time=300, is_personal=False)


@router.message(Command('group'))
async def a(message: Message) -> None:
    await message.bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
    group = message.text.split(' ')[1]
    date: datetime.datetime = datetime.datetime.fromtimestamp(float(message.text.split(' ')[2]))
    monday_date = date.date() - datetime.timedelta(days=date.weekday())
    await message.answer(
        f"🎓 Расписание группы {group}\n\n🗓️ {date.weekday()}, {date.day} {date.month}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
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
                ]
            # [
            #     InlineKeyboardButton(text="ПН", callback_data=f'group monday {group} {monday_date}'),
            #     InlineKeyboardButton(text="ВТ", callback_data=f'group tuesday {group} {monday_date + datetime.timedelta(days=1)}'),
            #     InlineKeyboardButton(text="СР", callback_data=f'group wednesday {group} {monday_date + datetime.timedelta(days=2)}')
            # ],
            # [
            #     InlineKeyboardButton(text="ЧТ", callback_data=f'group thursday {group} {monday_date + datetime.timedelta(days=3)}'),
            #     InlineKeyboardButton(text="ПТ", callback_data=f'group friday {group} {monday_date + datetime.timedelta(days=4)}'),
            #     InlineKeyboardButton(text="СБ", callback_data=f'group saturday {group} {monday_date + datetime.timedelta(days=4)}')
            # ],
            # [
            #     InlineKeyboardButton(text="Пред.неделя⬅️", callback_data=f"group week {group} {monday_date - datetime.timedelta(days=7)}"),
            #     InlineKeyboardButton(text="Сегодня",callback_data= f'group today {group}'),
            #     InlineKeyboardButton(text="След.неделя➡️", callback_data=f"group week {group} {monday_date + datetime.timedelta(days=7)}")
            # ]
        ]), )


@router.message(Command('find'))
async def a(message: Message) -> None:
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔎 Расширенный поиск", switch_inline_query_current_chat=" ")]
    ])
    await message.answer("✏️ Введите группу или преподавателя, или воспользуйтесь расширенным поиском",
                         reply_markup=btn)


@router.message(Command('about'))
async def a(message: Message) -> None:
    await message.answer("Норм")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(
        router,
        navigation.router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
