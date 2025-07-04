from aiogram import Router, F
from aiogram.types import CallbackQuery


router = Router(name = 'misc_router')


@router.callback_query(F.data == 'delete_message')
async def delete_message(callback: CallbackQuery) -> None:
    await callback.bot.delete_message(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id
    )