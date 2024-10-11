import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from callbacks import navigation, search, test, parser, events
from callbacks.events import on_on, on_exit
from callbacks.parser import check_new
from secrets import TOKEN

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    scheduler = AsyncIOScheduler()
    trigger = CronTrigger(minute="0/15", hour="2-17")
    scheduler.add_job(check_new, trigger, args=(bot,))
    scheduler.start()

    dp.include_routers(
        navigation.router, search.router, test.router, parser.router, events.router
    )
    try:
        await on_on(bot=bot)
        await check_new(bot=bot)
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await on_exit(bot=bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
