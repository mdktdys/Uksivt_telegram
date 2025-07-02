import base64
import datetime
import traceback
import requests

from typing import List
from aiogram import Bot
from aiogram.types import BufferedInputFile, FSInputFile, Message
from aiogram.utils.media_group import MediaGroupBuilder
from requests import Response
from supabase import Client, create_client

from callbacks.events import on_check_end, on_check_start
from callbacks.tools import send_large_text
from DTOmodels.schemas import (
    CheckResultCheckExisting,
    CheckResultFoundNew,
    CheckZamenaResultFailed,
    ZamenaParseFailedNotFoundItems,
    ZamenaParseSucess,
)
from models.search_result import DayScheduleFormatted
from my_secrets import (
    API_KEY,
    API_URL,
    DEBUG_CHANNEL,
    MAIN_CHANNEL,
    SCHEDULER_SUPABASE_ANON_KEY,
    SCHEDULER_SUPABASE_URL,
)
from utils.extensions import month_name, weekday_name


key: str = SCHEDULER_SUPABASE_ANON_KEY
url: str = SCHEDULER_SUPABASE_URL
supabase_connect: Client = create_client(url, key)


async def send_zamena_alert(
    bot: Bot, target_id: int, date, chat_id: int, target_type: int
) -> None:
    target_type_named = ''
    if target_type != 1 and target_type != 2:
        return
    if target_type == 1:
        target_type_named = "groups"
    if target_type == 2:
        target_type_named = "teachers"

    res: Response = requests.get(
        f'{API_URL}{target_type_named}/day_schedule_formatted/{target_id}/{datetime.datetime.now().strftime("%Y-%m-%d")}/',
        headers={"X-API-KEY": API_KEY}
    )
    
    response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(res.text)
    header: str = f"🎓 Изменения в расписании {response.search_name} по новым заменам\n"
    body: str = "\n".join(response.paras) if response.paras else "\n🎉 Нет пар"
    calendar_footer: str = f"\n📅 {weekday_name(date)}, {date.day} {month_name(date)}"
    await bot.send_message(
        chat_id=chat_id,
        text=f"{header}" f"{body}" f"\n{calendar_footer}"
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


def get_file_extension(url_: str) -> str:
    parts = url_.split("/")
    file_name = parts[-1]
    file_parts = file_name.split(".")
    if len(file_parts) > 1:
        return file_parts[-1]
    else:
        return ""

def get_targetIds_subscribers(target_ids: list[int], target_type: int) -> List[str]:
    result = (supabase_connect.table('Subscribers').select('chat_id').eq('target_type', target_type).in_('target_id', target_ids).execute())
    return [item['chat_id'] for item in result.data]


def download_file(link: str, filename: str) -> None:
    response = requests.get(link)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File '{filename}' has been downloaded successfully.")
    else:
        print("Failed to download the file.")


async def parse_zamena(bot: Bot, url_: str, date: datetime.date, notify: bool):
    message: str = ""
    res: Response = requests.post(f"{API_URL}parser/parse_zamena", headers={"X-API-KEY": API_KEY},
        json = {
            'url': f'{url_}',
            'date': f'{date}',
            'notify': notify
        }
    )
    try:
        response: dict = res.json()
        match response["result"]:
            case "error":
                if response["error"] == "Not found items":
                    message = f"⚠️ Ошибка парсинга замен\n\n{response['trace']}\n\nна {date}"
                    result = ZamenaParseFailedNotFoundItems.model_validate_json(res.text)
                    for e in result.items:
                        message = message + f"\n{e}\n"
            case "ok":
                result_success: ZamenaParseSucess = ZamenaParseSucess.model_validate_json(res.text)
                group_subscribers: list[str] = get_targetIds_subscribers(
                    target_ids= result_success.affected_groups,
                    target_type = 1
                )
                teacher_subscribers: list[str] = get_targetIds_subscribers(
                    target_ids = result_success.affected_teachers,
                    target_type = 2
                )
                from utils.sender import send_multicast_message
                await send_multicast_message(
                    chat_ids = group_subscribers + teacher_subscribers,
                    message = f"<a href='{url_}'>Появились замены для тебя! на {date}</a>" 
                )
                message = f"✅ Успешно спарсил замену\n\n{url_} на {date}"

                
        await send_large_text(
            bot=bot,
            chat_id = DEBUG_CHANNEL,
            text = message,
            max_length = 3000
        )
    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message

        await send_error_message(
            bot = bot,
            chat_id = DEBUG_CHANNEL,
            error_header = "Ошибка",
            application = "Kronos",
            time_ = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body = error_body,
        )


async def check_new_zamena(bot: Bot) -> None:
    try:
        message = ""
        zamenas = []
        await on_check_start(bot=bot)
        res: Response = requests.get(f"{API_URL}parser/check_new", headers={"X-API-KEY": API_KEY})
        try:
            response: dict = res.json()
            print(response)
            match response["result"]:
                case "FoundNew":
                    result: CheckResultFoundNew = CheckResultFoundNew.model_validate_json(res.text)
                    messages = []
                    for zamena in result.checks:
                        if zamena.result == "Failed":
                            messages.append(f"\n⚠️ Ошибка замены\n<pre>{zamena.error[0:200]}\n{zamena.trace[0:300]}</pre>")
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
                            sended_messages: List[Message] = await bot.send_media_group(
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
                                            msg.message_id for msg in sended_messages
                                        ],
                                    )
                                except Exception as e:
                                    print(e)
                            zamenas.append((zamena.link, zamena.date))
                        if zamena.result == "FailedDownload":
                            messages.append(f"\nНайдена\n{zamena.link}")
                            caption = f"Новые замены на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.link}'>Ссылка</a>"
                            sended_message: Message = await bot.send_message(
                                chat_id=MAIN_CHANNEL, text=caption
                            )
                            for sub in get_subscribers(
                                target_id=-1, target_type=-1
                            ):
                                try:
                                    await bot.forward_message(
                                        chat_id=sub,
                                        from_chat_id=MAIN_CHANNEL,
                                        message_id=sended_message.message_id,
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

                            sended_messages: List[Message] = await bot.send_media_group(
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
                                            msg.message_id for msg in sended_messages
                                        ],
                                    )
                                except Exception as e:
                                    print(e)
                            zamenas.append((zamena.link, zamena.date))
                    message = message.join(messages)
                case "Error":
                    result = CheckZamenaResultFailed.model_validate_json(res.text)
                    message = "\nОшибка"
                    raise Exception(result.error)
                case "CheckExisting":
                    result = CheckResultCheckExisting.model_validate_json(res.text)
                    messages = []

                    if len(result.checks) == 0:
                        message = "\nНичего нового"
                    else:
                        for zamena in result.checks:
                            if zamena.result == "Failed":
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
                                sended_messages: List[Message] = await bot.send_media_group(
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
                                                msg.message_id for msg in sended_messages
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
                                sended_message: Message = await bot.send_message(
                                    chat_id=MAIN_CHANNEL, text=caption
                                )
                                for sub in get_subscribers(
                                    target_id=-1, target_type=-1
                                ):
                                    try:
                                        await bot.forward_message(
                                            chat_id=sub,
                                            from_chat_id=MAIN_CHANNEL,
                                            message_id=sended_message.message_id,
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

                                sended_messages: List[Message] = await bot.send_media_group(chat_id=MAIN_CHANNEL, media=media_group.build())
                                for sub in get_subscribers(target_id=-1, target_type=-1):
                                    try:
                                        await bot.forward_messages(
                                            chat_id=sub,
                                            from_chat_id=MAIN_CHANNEL,
                                            message_ids=[
                                                msg.message_id for msg in sended_messages
                                            ],
                                        )
                                    except Exception as e:
                                        print(e)
                                zamenas.append((zamena.link, zamena.date))
                        message = message.join(messages)
                case "Checked":
                    message = "\nНичего нового"

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
            message: str = f"\n \n{e} {traceback.format_exc()}"
            print(e)
            print(traceback.format_exc())

        await on_check_end(bot=bot, result = message[0:2000])

        try:
            for zam in zamenas:
                await parse_zamena(bot=bot, date=zam[1], url_=zam[0], notify= True)
        except Exception as e:
            print(e)
            await bot.send_message(chat_id=DEBUG_CHANNEL, text=str(e))

    except Exception as e:
        error_body: str = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message

        await send_error_message(
            bot=bot,
            chat_id=DEBUG_CHANNEL,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )
