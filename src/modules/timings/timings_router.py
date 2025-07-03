from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from models.timings_model import Timings
from src.services.data_service import DataService
from src.services.assets_service import AssetsService
from .timings_keyboard import timings_keyboard, obed_timings_keyboard, saturday_timings_keyboard
from .timings_screen import timings_screen, saturday_timings_screen, obed_timings_screen


router = Router(name = 'timings_router')


@router.callback_query(F.data == 'timings_screen')
async def show_timings_screen(callback: CallbackQuery, data_service: DataService, assets_service: AssetsService) -> None:
    timings: list[Timings] = await data_service.get_timings()

    await callback.bot.edit_message_media(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        media = InputMediaPhoto(
            media = assets_service.get_image("timings_image"),
            caption = timings_screen(timings)
        ),
        reply_markup = timings_keyboard()
    )


@router.callback_query(F.data == 'obed_timings_screen')
async def show_obed_timings_screen(callback: CallbackQuery, data_service: DataService, assets_service: AssetsService) -> None:
    timings: list[Timings] = await data_service.get_timings()

    await callback.bot.edit_message_media(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        media = InputMediaPhoto(
            media = assets_service.get_image("obed_timings_image"),
            caption = obed_timings_screen(timings)
        ),
        reply_markup = obed_timings_keyboard()
    )


@router.callback_query(F.data == 'saturday_timings_screen')
async def show_saturday_timings_screen(callback: CallbackQuery, data_service: DataService, assets_service: AssetsService) -> None:
    timings: list[Timings] = await data_service.get_timings()

    await callback.bot.edit_message_media(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        media = InputMediaPhoto(
            media = assets_service.get_image("saturday_timings_image"),
            caption = saturday_timings_screen(timings)
        ),
        reply_markup = saturday_timings_keyboard()
    )