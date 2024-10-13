import base64
import datetime
import html
import traceback

import requests
from aiogram import Bot
import aiohttp
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from DTOmodels.schemas import CheckResultFoundNew, CheckResultCheckExisting
from callbacks.events import on_check_start, on_check_end
from my_secrets import DEBUG_CHANNEL, API_URL, API_KEY, MAIN_CHANNEL


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
                                        f"\nОшибка замены\n<pre>{zamena.error[0:200]}\n{zamena.trace[0:300]}</pre>"
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
                                    await bot.send_media_group(
                                        MAIN_CHANNEL, media=media_group.build()
                                    )
                                if zamena.result == "FailedDownload":
                                    messages.append(f"\nНайдена\n{zamena.link}")
                                    caption = f"Новые замены на <a href='{zamena.link}'>{zamena.date}</a>\n\n<a href='{zamena.link}'>Ссылка</a>"
                                    await bot.send_message(
                                        chat_id=MAIN_CHANNEL, text=caption
                                    )

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

                                    await bot.send_media_group(
                                        chat_id=MAIN_CHANNEL, media=media_group.build()
                                    )

                                    # subs = await r.lrange("subs", 0, -1)
                                    # for i in subs:
                                    #     try:
                                    #         await bot.send_media_group(i, media=media_group.build())
                                    #     except Exception as error:
                                    #         try:
                                    #             await bot.send_message(
                                    #                 chat_id=admins[0], text=str(error)
                                    #             )
                                    #         except:
                                    #             continue
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
                                        f"\nОшибка проверки замены\n<pre>{zamena.error[0:200]}\n{zamena.trace[0:300]}</pre>"
                                    )
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
