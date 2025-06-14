from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.menu_keyboard import menu_screen_keyboard, menu_screen

router = Router(name = 'menu_router')

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.bot.send_message(
        chat_id = message.chat.id,
        text = menu_screen(),
        reply_markup = menu_screen_keyboard()
    )
    
@router.callback_query(F.data == "menu_screen")
async def show_menu(callback: CallbackQuery) -> None:
     await callback.bot.edit_message_text(
        chat_id = callback.message.chat.id,
        text = menu_screen(),
        reply_markup = menu_screen_keyboard()
    )