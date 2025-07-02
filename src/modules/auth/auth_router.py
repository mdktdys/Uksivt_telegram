
from aiogram import F, Router
from aiogram.types import CallbackQuery


router = Router(name = 'auth_router')


@router.callback_query(F.data.startswith("auth_login"))
async def auth_login(callback: CallbackQuery) -> None:
    token: str = callback.data.split("|")[1]
    
    
    
    await callback.bot.send_message(
        chat_id = callback.message.chat.id,
        text = 'Успешная авторизация!'
    )