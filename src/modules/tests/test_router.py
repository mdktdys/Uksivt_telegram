from aiogram import Router
from aiogram.types import Message
from aiogram.types.chat_full_info import ChatFullInfo
from aiogram.types.chat_photo import ChatPhoto

from utils.logger import logger

router = Router(name = 'test_router')

@router.message()
async def handle_all(message: Message) -> None:
    if message.from_user is None or message.bot is None:
        return
    
    text_info: str = f'''
[{message.chat.full_name}]
[@{message.from_user.username if message.from_user.username else 'NoUsername'}]
{text if (text := message.text or message.caption) else ''}
    '''

    target_chat_id = -1002596787538

    try:
        await message.forward(chat_id=target_chat_id)
    except Exception:
        media: str | None = None

        if message.photo:
            media = message.photo[-1].file_id
            await message.bot.send_photo(
                chat_id = target_chat_id,
                photo = media,
                caption = text_info
            )
        elif message.video:
            media = message.video.file_id
            await message.bot.send_video(
                chat_id = target_chat_id,
                video = media,
                caption = text_info
            )
        elif message.document:
            media = message.document.file_id
            await message.bot.send_document(
                chat_id = target_chat_id,
                document = media,
                caption = text_info
            )
        elif message.audio:
            media = message.audio.file_id
            await message.bot.send_audio(
                chat_id = target_chat_id,
                audio = media,
                caption = text_info
            )
        elif message.voice:
            media = message.voice.file_id
            await message.bot.send_voice(
                chat_id = target_chat_id,
                voice = media,
                caption = text_info
            )
        elif message.sticker:
            await message.bot.send_sticker(
                chat_id = target_chat_id,
                sticker = message.sticker.file_id
            )
            await message.bot.send_message(
                chat_id = target_chat_id,
                text = text_info
            )
        else:
            await message.bot.send_message(
                chat_id = target_chat_id,
                text = text_info
            )
            await message.bot.send_message(
                chat_id = target_chat_id,
                text = text_info
            )            