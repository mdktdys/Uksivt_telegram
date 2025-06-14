from typing import Any, Dict
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.settings_keyboard import settings_screen, settings_screen_keyboard
from keyboards.change_name_keyboard import change_name_screen, change_name_screen_keyboard

router = Router(name = 'settings_router')

class SettingsStates(StatesGroup):
    waiting_for_name = State()


@router.callback_query(F.data == "settings_screen")
async def show_settings(callback: CallbackQuery) -> None:
    text: str = settings_screen()
    await callback.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    await callback.bot.send_message(text = text, chat_id = callback.message.chat.id, reply_markup = settings_screen_keyboard())
    
    
@router.callback_query(F.data == "change_name_screen")
async def show_change_name(callback: CallbackQuery, state: FSMContext) -> None:
    text: str = change_name_screen()
    await callback.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    await state.set_state(SettingsStates.waiting_for_name)
    await state.update_data(message_id = callback.message.message_id)
    await callback.bot.send_message(text = text, chat_id = callback.message.chat.id, reply_markup = change_name_screen_keyboard())
    
    
@router.message(SettingsStates.waiting_for_name)
async def process_name_input(message: Message, state: FSMContext) -> None:
    try:
        data: Dict[str, Any] = await state.get_data()
        message_id: int | None = data.get("message_id")

        name: str = message.text
        
        text: str = settings_screen()
        # await message.bot.delete_message(message_id = message_id, chat_id = message.chat.id)
        await message.bot.delete_message(message_id = message.message_id, chat_id = message.chat.id)
        await message.bot.send_message(
            chat_id = message.chat.id,
            text = text,
            reply_markup = settings_screen_keyboard()
        )
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное имя")