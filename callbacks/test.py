
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from my_secrets import API_KEY
import requests as req

router = Router()

@router.message(F.text, Command("auth"))
async def test(message: Message):
    response: list[dict] = req.get("http://fastapi:3000/auth/protected-route", headers={"X-API-KEY": API_KEY}).json()
    await message.answer(str(response))
