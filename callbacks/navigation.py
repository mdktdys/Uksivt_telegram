from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "monday")
async def show_monday(callback: CallbackQuery) -> None:
    print(callback)

    await callback.message.edit_text(
        "test"
    )
    await callback.answer()