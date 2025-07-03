from aiogram import F, Router
from aiogram.types import User, UserProfilePhotos, CallbackQuery
from aiogram.types.photo_size import PhotoSize
import aiohttp

router = Router(name = 'auth_router')


@router.callback_query(F.data.startswith("auth_login"))
async def auth_login(callback: CallbackQuery) -> None:
    token: str = callback.data.split("|")[1]
    user: User = callback.from_user
    photos: UserProfilePhotos = await callback.bot.get_user_profile_photos(user.id)
    photo: PhotoSize = photos.photos[0][0]

    await auth_user(
        token = token,
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        user_id = user.id,
        chat_id = callback.message.chat.id,
        photo_url = photo.file_id
    )
    
    await callback.bot.send_message(
        chat_id = callback.message.chat.id,
        text = 'Успешная авторизация!'
    )
    

async def auth_user(
    token: str,
    user_id: int,
    chat_id: int,
    photo_url: str,
    first_name: str,
    last_name: str,
    username: str
) -> None:
    url = "https://api.uksivt.xyz/api/v1/telegram/verify"
    data: dict[str, str] = {
        "token": token,
        'firstname': first_name,
        'lastname': last_name,
        'username': username,
        "user_id": user_id,
        "chat_id": chat_id,
        "photo_url": photo_url
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:
                print("User authenticated successfully.")
            else:
                print("Failed to authenticate user.")