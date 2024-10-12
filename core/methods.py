import base64
import datetime
import html
import io
import traceback

from aiogram import Bot
import aiohttp
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from DTOmodels.schemas import CheckResultFoundNew
from callbacks.events import on_check_start, on_check_end
from secrets import DEBUG_CHANNEL, API_URL, API_KEY, MAIN_CHANNEL


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
                    match response["result"]:
                        case "FoundNew":
                            result = CheckResultFoundNew.parse_obj(response)
                            message = "\n\nНовые замены\n"
                            messages = []
                            for zamena in result.checks:
                                print(zamena)
                                if zamena.result == "Failed":
                                    messages.append(
                                        f"\nОшибка замены\n{zamena.error[0:100]}\n{zamena.trace[0:100]}"
                                    )
                                if zamena.result == "Success":
                                    messages.append(f"\nНайдена\n{zamena.link[0:100]}")

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
                                    # for i in screenshot_paths:
                                    #     image = FSInputFile(i)
                                    #     media_group.add_photo(image)
                                    # try:
                                    #     # await bot.send_media_group(chat_id=admins[0], media=media_group.build())
                                    #
                            message = message.join(messages)
                        case "Failed":
                            result = CheckResultFoundNew.parse_obj(response)
                            message = "Ошибка"
                            print(result)

                except aiohttp.ContentTypeError:
                    print("Ответ не является JSON")

        await on_check_end(bot=bot, result=(str(html.escape(message[0:1000]))))

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
