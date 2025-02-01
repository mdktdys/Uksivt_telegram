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
from DTOmodels.schemas import (
    CheckResultFoundNew,
    CheckResultCheckExisting,
    ZamenaParseFailedNotFoundItems,
)
from callbacks.events import on_check_start, on_check_end
from callbacks.tools import send_large_text
from models.search_result import DayScheduleFormatted
from my_secrets import (
    DEBUG_CHANNEL,
    API_URL,
    API_KEY,
    MAIN_CHANNEL,
    SCHEDULER_SUPABASE_URL,
    SCHEDULER_SUPABASE_ANON_KEY,
)
from utils.extensions import weekday_name, month_name

key = SCHEDULER_SUPABASE_ANON_KEY
url = SCHEDULER_SUPABASE_URL
supabase_connect: Client = create_client(url, key)


# async def alert(bot: Bot):
#     res = [382, 383]
#     for sub in get_subscribers(target_id=-1, target_type=-1):
#         await bot.forward_messages(
#             chat_id=sub,
#             from_chat_id=MAIN_CHANNEL,
#             message_ids=res,
#         )


async def send_zamena_alert(
    bot: Bot, target_id: int, date, chat_id: int, target_type: int
):
    if target_type != 1 and target_type != 2:
        return
    if target_type == 1:
        target_type_named = "groups"
    if target_type == 2:
        target_type_named = "teachers"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(
            f'{API_URL}{target_type_named}/day_schedule_formatted/{target_id}/{datetime.datetime.now().strftime("%Y-%m-%d")}/',
            headers={"X-API-KEY": API_KEY},
        ) as res:
            response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(
                await res.text()
            )
    header = f"🎓 Изменения в расписании {response.search_name} по новым заменам\n"
    body = "\n".join(response.paras) if response.paras else "\n🎉 Нет пар"
    calendar_footer = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}"
    await bot.send_message(
        chat_id=chat_id, text=f"{header}" f"{body}" f"\n{calendar_footer}"
    )


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


async def parse_zamena(bot: Bot, url: str, date: datetime.date):
    message = ""
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
            f"{API_URL}parser/parse_zamena",
            headers={"X-API-KEY": API_KEY},
            json={"url": f"{url}", "date": f"{date}"},
        ) as res:
            try:
                response: dict = await res.json()
                print(response)
                match response["result"]:
                    case "error":
                        if response["error"] == "Not found items":
                            message = f"⚠️ Ошибка парсинга замен\n\n{response['trace']}\n\nна {date}"
                            result = ZamenaParseFailedNotFoundItems.parse_obj(response)
                            for e in result.items:
                                message = message + f"\n{e}\n"
                    case "ok":
                        message = f"✅ Успешно спарсил замену\n\n{url} на\n\n{date}"
                await send_large_text(
                    bot=bot, chat_id=DEBUG_CHANNEL, text=message, max_length=3000
                )
                # await bot.send_message(chat_id=DEBUG_CHANNEL, text=message)
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
        zamenas: List[(str, datetime)] = []
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
                                    for sub in get_subscribers(
                                        target_id=-1, target_type=-1
                                    ):
                                        try:
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                        except Exception as e:
                                            print(e)
                                    zamenas.append((zamena.link, zamena.date))
                                if zamena.result == "FailedDownload":
                                    messages.append(f"\nНайдена\n{zamena.link}")
                                    caption = f"Новые замены на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.link}'>Ссылка</a>"
                                    res: Message = await bot.send_message(
                                        chat_id=MAIN_CHANNEL, text=caption
                                    )
                                    for sub in get_subscribers(
                                        target_id=-1, target_type=-1
                                    ):
                                        try:
                                            await bot.forward_message(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_id=res.message_id,
                                            )
                                        except Exception as e:
                                            print(e)
                                    zamenas.append((zamena.link, zamena.date))
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
                                    for sub in get_subscribers(
                                        target_id=-1, target_type=-1
                                    ):
                                        try:
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                        except Exception as e:
                                            print(e)
                                    zamenas.append((zamena.link, zamena.date))
                            message = message.join(messages)
                        case "Error":
                            result = CheckZamenaResultFailed.parse_obj(response)
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
                                    for sub in get_subscribers(
                                        target_id=-1, target_type=-1
                                    ):
                                        try:
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                        except Exception as e:
                                            print(e)
                                    zamenas.append((zamena.link, zamena.date))
                                if zamena.result == "FailedDownload":
                                    messages.append(
                                        f"\nОбнаружен перезалив\n{zamena.link}"
                                    )
                                    caption = f"Обнаружен перезалив на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.link}'>Ссылка</a>"
                                    res: Message = await bot.send_message(
                                        chat_id=MAIN_CHANNEL, text=caption
                                    )
                                    for sub in get_subscribers(
                                        target_id=-1, target_type=-1
                                    ):
                                        try:
                                            await bot.forward_message(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_id=res.message_id,
                                            )
                                        except Exception as e:
                                            print(e)
                                            pass
                                    zamenas.append((zamena.link, zamena.date))
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
                                    for sub in get_subscribers(
                                        target_id=-1, target_type=-1
                                    ):
                                        try:
                                            await bot.forward_messages(
                                                chat_id=sub,
                                                from_chat_id=MAIN_CHANNEL,
                                                message_ids=[
                                                    msg.message_id for msg in res
                                                ],
                                            )
                                        except Exception as e:
                                            print(e)
                                    zamenas.append((zamena.link, zamena.date))
                            message = message.join(messages)
                        case "Checked":
                            message = "\nНичего нового"

                except aiohttp.ContentTypeError:
                    print("Ответ не является JSON")

        await on_check_end(bot=bot, result=message[0:2000])
        try:
            for zam in zamenas:
                await parse_zamena(bot=bot, date=zam[1], url=zam[0])
        except Exception as e:
            print(e)
            await bot.send_message(chat_id=DEBUG_CHANNEL, text=str(e))

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
