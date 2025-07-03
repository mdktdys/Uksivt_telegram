from aiogram import F, Router
from aiogram.types import User, UserProfilePhotos, CallbackQuery
from aiogram.types.photo_size import PhotoSize
import aiohttp
from typing import Optional, Any

router = Router(name = 'auth_router')


@router.callback_query(F.data.startswith("auth_login"))
async def auth_login(callback: CallbackQuery) -> None:
    token: str = callback.data.split("|")[1]
    user: User = callback.from_user
    photos: UserProfilePhotos = await callback.bot.get_user_profile_photos(user.id)
    print(photos)
    # photo: PhotoSize = photos.photos[0]

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
        print(e)
        await callback.bot.send_message(
            chat_id = callback.message.chat.id,
            text = 'Ошибка авторизации! ' + str(e)
        )
        return

    await callback.bot.send_message(
        chat_id = callback.message.chat.id,
        text = 'Успешная авторизация!'
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
    url = "https://api.uksivt.xyz/api/v1/telegram/verify"
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
        async with session.post(url, json = data) as response:
            if response.status == 201:
                print("User authenticated successfully.")
            else:
                raise Exception(str(response))