import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from callbacks import navigation, search, test, parser, events
from callbacks.events import on_on, on_exit
from core.methods import check_new_zamena
from secrets import TOKEN

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    scheduler = AsyncIOScheduler()
    trigger = CronTrigger(minute="0/2", hour="6-23", timezone="Asia/Yekaterinburg")
    scheduler.add_job(check_new_zamena, trigger, args=(bot,))
    scheduler.start()

    dp.include_routers(
        navigation.router, search.router, test.router, parser.router, events.router
    )
    try:
        await dp.start_polling(bot)
        await on_on(bot=bot)
        await check_new_zamena(bot=bot)
    finally:
        scheduler.shutdown()
        await on_exit(bot=bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
