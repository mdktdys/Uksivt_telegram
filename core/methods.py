import datetime
import traceback

from aiogram import Bot
import aiohttp
from callbacks.events import on_check_start, on_check_end
from secrets import DEBUG_CHANNEL, API_URL, API_KEY


async def check_new_zamena(bot: Bot):
    try:
        await on_check_start(bot=bot)

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                f"{API_URL}parser/check_new",
                headers={"X-API-KEY": API_KEY},
            ) as res:
                response = res

        await on_check_end(bot=bot)
        return response

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
