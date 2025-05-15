
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(F.text, Command("auth"))
async def test(message: Message):
    date = '15.05.2025'
    url_ = 'https://uksivt.ru/wp-content/uploads/2025/05/15.05.pdf'
    message_: str = f"<a href='{url_}'>Появились замены для тебя! на {date}</a>"
    await message.bot.send_message(
        chat_id = message.chat.id,
        text = message_
    )
