from typing import Any, Optional

import aiohttp
from aiogram import F, Router
from aiogram.types import CallbackQuery, User

from my_secrets import API_KEY

from .auth_keyboard import auth_success_keyboard

router = Router(name = 'auth_router')


@router.callback_query(F.data.startswith("auth_login"))
async def auth_login(callback: CallbackQuery) -> None:
    if callback.data is None:
        return

    token: str = callback.data.split("|")[1]
    user: User = callback.from_user

    try:
        await auth_user(
            token = token,
            first_name = user.first_name if user.first_name is not None else None,
            last_name = user.last_name if user.last_name is not None else None,
            username = user.username if user.username is not None else None,
            user_id = str(user.id),
            chat_id = str(callback.message.chat.id),
            photo_url = ''
        )
    except Exception as e:
        await callback.bot.edit_message_text(
            chat_id = callback.message.chat.id,
            message_id = callback.message.message_id,
            text = 'Ошибка авторизации!' + str(e),
            reply_markup = auth_success_keyboard()
        )
        return

    await callback.bot.edit_message_text(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        text = '✅ Успешная авторизация!',
        reply_markup = auth_success_keyboard()
    )
    

async def auth_user(
    token: str,
    user_id: int,
    chat_id: int,
    photo_url: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None
) -> None:
    url = "https://api.uksivt.xyz/v1/telegram_auth/verify_token"
    data: dict[str, Any] = {
        "token": token,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "user_id": user_id,
        "chat_id": chat_id,
        "photo_url": photo_url
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json = data, headers={'x-api-key':API_KEY}) as response:
            if response.status == 201:
                print("User authenticated successfully.")
            else:
                raise Exception(str(response))