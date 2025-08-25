from typing import Any, BinaryIO, Optional

import aiohttp
from aiogram import F, Router
from aiogram.types import CallbackQuery, ChatFullInfo, ChatPhoto, User
from aiogram.types.file import File
from aiogram.types.user_profile_photos import UserProfilePhotos

from my_secrets import API_KEY

from .auth_keyboard import auth_success_keyboard

router = Router(name = 'auth_router')


@router.callback_query(F.data.startswith("auth_login"))
async def auth_login(callback: CallbackQuery) -> None:
    if callback.data is None or callback.bot is None:
        return

    token: str = callback.data.split("|")[1]
    user: User = callback.from_user

    try:
        chat_info: ChatFullInfo = await callback.bot.get_chat(chat_id = callback.from_user.id)
        photo: ChatPhoto | None = chat_info.photo
        
        if photo is None:
            return
        
        file: File = await callback.bot.get_file(photo.small_file_id)
        photo_bytes: BinaryIO | bytes | None = await callback.bot.download_file(file.file_path)
        
        if photo_bytes is None:
            return
        
        if hasattr(photo_bytes, "read"):
            photo_bytes = photo_bytes.read()
        
        await auth_user(
            token = token,
            first_name = user.first_name if user.first_name is not None else None,
            last_name = user.last_name if user.last_name is not None else None,
            username = user.username if user.username is not None else None,
            user_id = str(user.id),
            chat_id = str(callback.message.chat.id),
            photo_bytes = photo_bytes
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
        text = '✅ Успешная авторизация!\nМожете вернуться на страницу',
        reply_markup = auth_success_keyboard()
    )
    

async def auth_user(
    token: str,
    user_id: int,
    chat_id: int,
    photo_bytes: Optional[bytes] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None
) -> None:
    url = "https://api.uksivt.xyz/v1/telegram_auth/verify_token"

    if photo_bytes:
        form = aiohttp.FormData()
        form.add_field('token', token)
        form.add_field('first_name', first_name or "")
        form.add_field('last_name', last_name or "")
        form.add_field('username', username or "")
        form.add_field('user_id', user_id)
        form.add_field('chat_id', chat_id)
        form.add_field('photo', photo_bytes, filename='avatar.jpg', content_type='image/jpeg')

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data = form, headers={'x-api-key':API_KEY}) as response:
                if response.status == 201:
                    print("User authenticated successfully.")
                else:
                    raise Exception(await response.text())
    else:
        data: dict[str, Any] = {
            "token": token,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "user_id": user_id,
            "chat_id": chat_id,
            "photo_url": None
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json = data, headers={'x-api-key':API_KEY}) as response:
                if response.status == 201:
                    print("User authenticated successfully.")
                else:
                    raise Exception(await response.text())