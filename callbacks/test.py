import datetime
import html
import traceback

import requests
from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from secrets import API_URL, API_KEY
import requests as req
router = Router()

# from broker import telegram_celery_app

#
# @router.message(F.text,Command("celery"))
# async def my_handler(message: Message):
#     try:
#         celery_app.send_task("app.ping", args=[datetime.datetime.now()])
#         await message.answer(f"Отправлено в очередь")
#     except Exception as e:
#         error_body = f"{str(e)}\n\n{traceback.format_exc()}"
#         await send_error_message(
#             bot=message.bot,
#             chat_id=message.chat.id,
#             error_header="Ошибка",
#             application="Parser",
#             time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
#             error_body=error_body,
#         )


@router.message(F.text,Command("auth"))
async def test(message: Message):
    print(API_KEY)
    response: list[dict] = req.get(f"http://fastapi:3000/auth/protected-route",headers={'X-API-KEY':API_KEY}).json()
    print(response)
    await message.answer(str(response))
