import aiohttp
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message

from DTOmodels.schemas import Subscription
from models.search_result_callback import Notification
from my_secrets import API_URL, API_KEY

router = Router()

@router.message(Command("sub"))
async def sub(message: Message):
    subscribtion = Subscription(
        chat_id=str(message.chat.id), target_id=-1, target_type=-1
    )
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                f"{API_URL}telegram/subscribe_zamena_notifications",
                headers={"X-API-KEY": API_KEY},
                json={
                    "chat_id": subscribtion.chat_id,
                    "target_type": subscribtion.target_type,
                    "target_id": subscribtion.target_id,
                },
            ) as res:
                print(res)
                if res.status == 201:
                    await message.answer("Подписан")
                if res.status == 202:
                    await message.answer("Вы уже подписаны")
    except Exception as error:
        await message.answer(f"Ошибка подписки\n{error}")


@router.message(Command("unsub"))
async def unsub(message: Message):
    subscribtion = Subscription(
        chat_id=str(message.chat.id), target_id=-1, target_type=-1
    )
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                f"{API_URL}telegram/unsubscribe_zamena_notifications",
                headers={"X-API-KEY": API_KEY},
                json={
                    "chat_id": subscribtion.chat_id,
                    "target_type": subscribtion.target_type,
                    "target_id": subscribtion.target_id,
                },
            ) as res:
                print(res)
                if res.status == 201:
                    await message.answer("Отписан")
                else:
                    await message.answer((await res.text()))
    except Exception as error:
        await message.answer(f"Ошибка отписки\n{error}")


@router.message()
def hangle(message: Message):
    message.forward(chat_id = -1002596787538)