
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(F.text, Command("auth"))
async def test(message: Message):
    await message.bot.send_message(
        chat_id = message.chat.id,
        text = 'test'
    )
