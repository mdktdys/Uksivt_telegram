from aiogram.types import Message
from .auth_keyboard import auth_keyboard


async def handle_auth(message: Message) -> None:
    token: str | None = message.text.split(" ")[1]

    if token is None:
        return
    
    await message.bot.send_message(
        chat_id=message.chat.id,
        text = "Нажмите для авторизации",
        reply_markup = auth_keyboard(token = token)
    )