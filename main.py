import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.handlers import InlineQueryHandler
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputMessageContent, InputTextMessageContent
import requests as req

from models import Group

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7283968288:AAEdrChiKr149d2p5zeoVZ29bWEJIFlDtTs"
API_URL = "https://api.uksivt.xyz/api/v1/"
# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")

@dp.inline_query()
async def handle(query: InlineQuery):
    filter_text = query.query
    if(filter_text == '' or filter_text is None):
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
    if(len(res) == 0):
        return query.answer([InlineQueryResultArticle(
            id=str(-1),
            title="Нет результатов",
            description="Попробуй что-то другое",
            url='uksivt.xyz',
            thumbnail_url='https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/python_(1).png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL3B5dGhvbl8oMSkucG5nIiwiaWF0IjoxNzIwMzg2MDg0LCJleHAiOjE3NTE5MjIwODR9.Xn_fkGftIEKCGFwQRK8JY0HPNnJax6uU8RtxmDUD0A0&t=2024-07-07T21%3A01%3A23.755Z',
            input_message_content=InputTextMessageContent(message_text='что я выбрал', )
        )], cache_time=1, is_personal=True)
    if(len(res) > 50):
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
        print(group)
        results.append(
            InlineQueryResultArticle(
                id=str(group.id),
                title=group.name,
                url='uksivt.xyz',
                thumbnail_url='https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/python_(1).png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL3B5dGhvbl8oMSkucG5nIiwiaWF0IjoxNzIwMzg2MDg0LCJleHAiOjE3NTE5MjIwODR9.Xn_fkGftIEKCGFwQRK8JY0HPNnJax6uU8RtxmDUD0A0&t=2024-07-07T21%3A01%3A23.755Z',
                input_message_content=InputTextMessageContent(message_text='что я выбрал', )
            )
        )

    await query.answer(results, cache_time=1, is_personal=True)


@dp.message(Command('a'))
async def a(message: Message) -> None:
    await message.answer("what")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())