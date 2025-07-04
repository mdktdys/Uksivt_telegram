from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.menu_keyboard import menu_screen_keyboard, menu_screen
from src.modules.auth.auth_handler import handle_auth
from src.services.assets_service import AssetsService
from models.user_model import User

router = Router(name = 'menu_router')

@router.message(CommandStart())
async def command_start_handler(message: Message, assets_service: AssetsService, user: User) -> None:
    if message.text.__contains__('auth'):
        await handle_auth(message = message)
        return
    
    await message.bot.send_photo(
        chat_id = message.chat.id,
        caption = menu_screen(user = user),
        photo = assets_service.get_image("menu_image"),
        reply_markup = menu_screen_keyboard()
    )


@router.callback_query(F.data == "menu_screen")
async def show_menu(callback: CallbackQuery, assets_service: AssetsService, user: User) -> None:
    await callback.bot.delete_message(message_id = callback.message.message_id, chat_id = callback.message.chat.id)
    await callback.bot.send_photo(
        chat_id = callback.message.chat.id,
        photo = assets_service.get_image("menu_image"),
        caption = menu_screen(user = user),
        reply_markup = menu_screen_keyboard()
    )