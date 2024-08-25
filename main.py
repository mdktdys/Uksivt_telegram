import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from callbacks import navigation, search

TOKEN = "7283968288:AAEdrChiKr149d2p5zeoVZ29bWEJIFlDtTs"
API_URL = "https://api.uksivt.xyz/api/v1/"


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(
        navigation.router,
        search.router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
