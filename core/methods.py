import datetime
import traceback

from aiogram import Bot
import aiohttp

from DTOmodels.schemas import CheckResultFoundNew
from callbacks.events import on_check_start, on_check_end
from secrets import DEBUG_CHANNEL, API_URL, API_KEY


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
                            message = "Новые замены"
                            print(result)
                        case "Failed":
                            result = CheckResultFoundNew.parse_obj(response)
                            message = "Ошибка"
                            print(result)

                except aiohttp.ContentTypeError:
                    print("Ответ не является JSON")

        await on_check_end(bot=bot, result=(str(message[0:300])))

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
