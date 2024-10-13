import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from DTOmodels.schemas import Subscription
from my_secrets import API_URL, API_KEY

router = Router()


@router.message(Command("sub"))
async def my_handlerr(message: Message):
    subscribtion = Subscription(
        chat_id=str(message.chat.id), target_id=-1, target_type=-1
    )
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                f"{API_URL}telegram/subscribe_zamena_notifications",
                headers={"X-API-KEY": API_KEY},
                data=subscribtion.model_dump_json(),
            ) as res:
                if res.status == 201:
                    await message.answer("Подписан")
                else:
                    await message.answer("Вы уже подписаны")
    except Exception as error:
        await message.answer(f"Ошибка подписки\n{error}")


@router.message(Command("unsub"))
async def my_handlers(message: Message):
    subscribtion = Subscription(
        chat_id=str(message.chat.id), target_id=-1, target_type=-1
    )
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                f"{API_URL}telegram/unsubscribe_zamena_notifications",
                headers={"X-API-KEY": API_KEY},
                data=subscribtion.model_dump_json(),
            ) as res:
                if res.status == 201:
                    await message.answer("Отписан")
                else:
                    await message.answer("Ошибка отписки")
    except Exception as error:
        await message.answer(f"Ошибка отписки\n{error}")
