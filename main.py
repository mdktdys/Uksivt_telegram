import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from callbacks import navigation, search, test, parser, events
from callbacks.events import on_on, on_exit
from secrets import TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    dp.include_routers(
        navigation.router, search.router, test.router, parser.router, events.router
    )
    try:
        await on_on(bot=bot)
        await dp.start_polling(bot)
    finally:
        await on_exit(bot=bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
