import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from callbacks import navigation, search

TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
API_URL = os.environ.get("TELEGRAM_API_URL")


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
