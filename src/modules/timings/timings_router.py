from aiogram import Router, F
from aiogram.types import CallbackQuery
from models.timings_model import Timings
from src.services.data_service import DataService
from .timings_keyboard import timings_keyboard
from .timings_screen import timings_screen


router = Router(name = 'timings_router')


@router.callback_query(F.data == 'timings_screen')
async def show_timings_screen(callback: CallbackQuery, data_service: DataService):
    timings: list[Timings] = await data_service.get_timings()

    await callback.bot.edit_message_text(
        text = timings_screen(timings),
        reply_markup = timings_keyboard()
    )


@router.callback_query(F.data == 'obed_timings_screen')
async def show_obed_timings_screen(callback: CallbackQuery, data_service: DataService):
    timings: list[Timings] = await data_service.get_timings()

    await callback.bot.edit_message_text(
        text = timings_screen(timings),
        reply_markup = timings_keyboard()
    )


@router.callback_query(F.data == 'saturday_timings_screen')
async def show_saturday_timings_screen(callback: CallbackQuery, data_service: DataService):
    timings: list[Timings] = await data_service.get_timings()

    await callback.bot.edit_message_text(
        text = timings_screen(timings),
        reply_markup = timings_keyboard()
    )