import base64
import datetime
import html
import traceback
from typing import List

import requests
from aiogram import Bot
import aiohttp
from aiogram.types import FSInputFile, BufferedInputFile, Message
from aiogram.utils.media_group import MediaGroupBuilder
from supabase import create_client, Client
from DTOmodels.schemas import CheckResultFoundNew, CheckResultCheckExisting
from callbacks.events import on_check_start, on_check_end
from callbacks.parser import admins
from my_secrets import (
    DEBUG_CHANNEL,
    API_URL,
    API_KEY,
    MAIN_CHANNEL,
    SCHEDULER_SUPABASE_URL,
    SCHEDULER_SUPABASE_ANON_KEY,
)

key = SCHEDULER_SUPABASE_ANON_KEY
url = SCHEDULER_SUPABASE_URL
supabase_connect: Client = create_client(url, key)


def get_subscribers(target_type: int, target_id: int) -> List[str]:
    res = (
        supabase_connect.table("Subscribers")
        .select("chat_id")
        .eq("target_type", target_type)
        .eq("target_id", target_id)
        .execute()
    )
    return [item["chat_id"] for item in res.data]


def get_file_extension(url):
    parts = url.split("/")
    file_name = parts[-1]
    file_parts = file_name.split(".")
    if len(file_parts) > 1:
        return file_parts[-1]
    else:
        return ""


def download_file(link: str, filename: str):
    response = requests.get(link)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File '{filename}' has been downloaded successfully.")
    else:
        print("Failed to download the file.")


async def parse_zamena(bot: Bot, url: str, date: datetime.datetime):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
            f"{API_URL}parser/parse_zamena",
            headers={"X-API-KEY": API_KEY},
            data={"url": f"{url}", "date": f"{date}"},
        ) as res:
            try:
                response: dict = await res.json()
                print(response)
                await bot.send_message(chat_id=DEBUG_CHANNEL, text=str(response))
            except Exception as e:
                error_body = f"{str(e)}\n\n{traceback.format_exc()}"
                from utils.sender import send_error_message

                await send_error_message(
                    bot=bot,
                    chat_id=DEBUG_CHANNEL,
                    error_header="Ошибка",
                    application="Kronos",
                    time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
                    error_body=error_body,
                )


async def check_new_zamena(bot: Bot):
    try:
        message = ""
        await on_check_start(bot=bot)

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                f"{API_URL}parser/check_new",
                headers={"X-API-KEY": API_KEY},
            ) as res:
                try:
                    response: dict = await res.json()
                    print(response)
                    match response["result"]:
                        case "FoundNew":
                            result = CheckResultFoundNew.parse_obj(response)
                            messages = []
                            for zamena in result.checks:
                                print(zamena)
                                if zamena.result == "Failed":
                                    messages.append(
                                        f"\n⚠️ Ошибка замены\n<pre>{zamena.error[0:200]}\n{zamena.trace[0:300]}</pre>"
                                    )
                                if zamena.result == "Success":
                                    messages.append(f"\nНайдена\n{zamena.link}")

                                    media_group = MediaGroupBuilder(
                                        caption=f"Новые замены на <a href='{zamena.link}'>{zamena.date}</a>  "
                                    )
                                    for image in zamena.images:
                                        image_data = base64.b64decode(image)
                                        img = BufferedInputFile(
                                            image_data, "temp_image.jpg"
                                        )
                                        media_group.add_photo(img)
                                    res: List[Message] = await bot.send_media_group(
                                        MAIN_CHANNEL, media=media_group.build()
                                    )
                                    print(res)
                                    try:
                                        for sub in get_subscribers(
                                            target_id=-1, target_type=-1
                                        ):
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                            # await bot.send_media_group(
                                            #     chat_id=sub, media=media_group.build()
                                            # )
                                    except:
                                        pass
                                if zamena.result == "FailedDownload":
                                    messages.append(f"\nНайдена\n{zamena.link}")
                                    caption = f"Новые замены на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.link}'>Ссылка</a>"
                                    res: Message = await bot.send_message(
                                        chat_id=MAIN_CHANNEL, text=caption
                                    )
                                    try:
                                        for sub in get_subscribers(
                                            target_id=-1, target_type=-1
                                        ):
                                            # await bot.send_message(
                                            #     chat_id=sub, text=caption
                                            # )
                                            await bot.forward_message(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_id=res.message_id,
                                            )
                                    except:
                                        pass
                                if zamena.result == "InvalidFormat":
                                    messages.append(f"\nНайдена\n{zamena.link}")
                                    caption = f"Новые замены на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.file}'>Ссылка на файлик</a>"

                                    media_group = MediaGroupBuilder(caption=caption)

                                    file_extension = get_file_extension(zamena.link)
                                    file_name = f"{zamena.date}.{file_extension}"
                                    download_file(
                                        link=zamena.link,
                                        filename=file_name,
                                    )
                                    media_group.add_document(
                                        FSInputFile(
                                            path=file_name,
                                            filename=f"{zamena.date}.{file_extension}",
                                        )
                                    )

                                    res: List[Message] = await bot.send_media_group(
                                        chat_id=MAIN_CHANNEL, media=media_group.build()
                                    )
                                    try:
                                        for sub in get_subscribers(
                                            target_id=-1, target_type=-1
                                        ):
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                            # await bot.send_media_group(
                                            #     chat_id=sub, media=media_group.build()
                                            # )
                                    except:
                                        pass
                            message = message.join(messages)
                        case "Failed":
                            result = CheckResultFoundNew.parse_obj(response)
                            message = "\nОшибка"
                            print(result)
                        case "CheckExisting":
                            print("HERE")
                            result = CheckResultCheckExisting.parse_obj(response)
                            message = "\nОшибка"
                            messages = []
                            for zamena in result.checks:
                                if zamena.result == "Failed":
                                    print("da")
                                    messages.append(
                                        f"\n⚠️ Ошибка проверки замены\n<pre>{zamena.error[0:200]}\n{zamena.trace[0:300]}</pre>"
                                    )
                                if zamena.result == "Success":
                                    messages.append(
                                        f"\nОбнаружен перезалив\n{zamena.link}"
                                    )

                                    media_group = MediaGroupBuilder(
                                        caption=f"Обнаружен перезалив на <a href='{zamena.link}'>{zamena.date}</a>  "
                                    )
                                    for image in zamena.images:
                                        image_data = base64.b64decode(image)
                                        img = BufferedInputFile(
                                            image_data, "temp_image.jpg"
                                        )
                                        media_group.add_photo(img)
                                    res: List[Message] = await bot.send_media_group(
                                        MAIN_CHANNEL, media=media_group.build()
                                    )
                                    try:
                                        for sub in get_subscribers(
                                            target_id=-1, target_type=-1
                                        ):
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                            # await bot.send_media_group(
                                            #     chat_id=sub, media=media_group.build()
                                            # )
                                    except:
                                        pass
                                if zamena.result == "FailedDownload":
                                    messages.append(
                                        f"\nОбнаружен перезалив\n{zamena.link}"
                                    )
                                    caption = f"Обнаружен перезалив на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.link}'>Ссылка</a>"
                                    res: Message = await bot.send_message(
                                        chat_id=MAIN_CHANNEL, text=caption
                                    )
                                    try:
                                        for sub in get_subscribers(
                                            target_id=-1, target_type=-1
                                        ):
                                            await bot.forward_message(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_id=res.message_id,
                                            )
                                            # await bot.send_message(
                                            #     chat_id=sub, text=caption
                                            # )
                                    except:
                                        pass
                                if zamena.result == "InvalidFormat":
                                    messages.append(
                                        f"\nОбнаружен перезалив\n{zamena.link}"
                                    )
                                    caption = f"Обнаружен перезалив на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.file}'>Ссылка на файлик</a>"

                                    media_group = MediaGroupBuilder(caption=caption)

                                    file_extension = get_file_extension(zamena.link)
                                    file_name = f"{zamena.date}.{file_extension}"
                                    download_file(
                                        link=zamena.link,
                                        filename=file_name,
                                    )
                                    media_group.add_document(
                                        FSInputFile(
                                            path=file_name,
                                            filename=f"{zamena.date}.{file_extension}",
                                        )
                                    )

                                    res: List[Message] = await bot.send_media_group(
                                        chat_id=MAIN_CHANNEL, media=media_group.build()
                                    )
                                    try:
                                        for sub in get_subscribers(
                                            target_id=-1, target_type=-1
                                        ):
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                    except:
                                        pass
                            message = message.join(messages)
                        case "Checked":
                            message = "\nНичего нового"

                except aiohttp.ContentTypeError:
                    print("Ответ не является JSON")

        await on_check_end(bot=bot, result=message[0:2000])

    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message

        await send_error_message(
            bot=bot,
            chat_id=DEBUG_CHANNEL,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )
