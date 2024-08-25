from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from aiogram.filters import Command

router = Router()


@router.message(Command('find'))
async def a(message: Message) -> None:
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔎 Расширенный поиск", switch_inline_query_current_chat=" ")]
    ])
    await message.answer("✏️ Введите группу или преподавателя, или воспользуйтесь расширенным поиском",
                         reply_markup=btn)


@router.message(Command('about'))
async def a(message: Message) -> None:
    await message.answer("Норм")