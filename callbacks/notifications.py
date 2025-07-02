import aiohttp
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message

from DTOmodels.schemas import Subscription
from models.search_result_callback import Notification
from my_secrets import API_URL, API_KEY

router = Router()

@router.message(Command("sub"))
async def sub(message: Message):
    subscribtion = Subscription(
        chat_id=str(message.chat.id), target_id=-1, target_type=-1
    )
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                f"{API_URL}telegram/subscribe_zamena_notifications",
                headers={"X-API-KEY": API_KEY},
                json={
                    "chat_id": subscribtion.chat_id,
                    "target_type": subscribtion.target_type,
                    "target_id": subscribtion.target_id,
                },
            ) as res:
                print(res)
                if res.status == 201:
                    await message.answer("Подписан")
                if res.status == 202:
                    await message.answer("Вы уже подписаны")
    except Exception as error:
        await message.answer(f"Ошибка подписки\n{error}")


@router.message(Command("unsub"))
async def unsub(message: Message):
    subscribtion = Subscription(
        chat_id=str(message.chat.id), target_id=-1, target_type=-1
    )
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                f"{API_URL}telegram/unsubscribe_zamena_notifications",
                headers={"X-API-KEY": API_KEY},
                json={
                    "chat_id": subscribtion.chat_id,
                    "target_type": subscribtion.target_type,
                    "target_id": subscribtion.target_id,
                },
            ) as res:
                print(res)
                if res.status == 201:
                    await message.answer("Отписан")
                else:
                    await message.answer((await res.text()))
    except Exception as error:
        await message.answer(f"Ошибка отписки\n{error}")


@router.message()
async def handle_all(message: Message):
    # Сбор информации об отправителе
    text_info = f'''
[{message.chat.full_name}]
[@{message.from_user.username if message.from_user.username else 'NoUsername'}]
{text if (text := message.text or message.caption) else ''}
    '''

    # ID чата, куда пересылаются сообщения
    target_chat_id = -1002596787538

    # Пересылка сообщения как есть (сохраняет автора и медиа)
    try:
        await message.forward(chat_id=target_chat_id)
    except Exception:
        # Если пересылка не удалась — пробуем вручную отправить с информацией
        media = None

        if message.photo:
            media = message.photo[-1].file_id
            await message.bot.send_photo(chat_id=target_chat_id, photo=media, caption=text_info)
        elif message.video:
            media = message.video.file_id
            await message.bot.send_video(chat_id=target_chat_id, video=media, caption=text_info)
        elif message.document:
            media = message.document.file_id
            await message.bot.send_document(chat_id=target_chat_id, document=media, caption=text_info)
        elif message.audio:
            media = message.audio.file_id
            await message.bot.send_audio(chat_id=target_chat_id, audio=media, caption=text_info)
        elif message.voice:
            media = message.voice.file_id
            await message.bot.send_voice(chat_id=target_chat_id, voice=media, caption=text_info)
        elif message.sticker:
            await message.bot.send_sticker(chat_id=target_chat_id, sticker=message.sticker.file_id)
            await message.bot.send_message(chat_id=target_chat_id, text=text_info)
        else:
            # На случай неизвестного формата
            await message.bot.send_message(chat_id=target_chat_id, text=text_info)