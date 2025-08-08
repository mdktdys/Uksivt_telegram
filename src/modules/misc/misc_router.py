from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router(name = 'misc_router')


@router.callback_query(F.data == 'delete_message')
async def delete_message(callback: CallbackQuery) -> None:
    if callback.bot is None or callback.message is None:
        return

    await callback.bot.delete_message(
        message_id = callback.message.message_id,
        chat_id = callback.message.chat.id
    )