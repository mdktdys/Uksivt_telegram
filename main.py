import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from callbacks import navigation, search, test, parser, events, notifications
from callbacks.events import on_on, on_exit
from core.methods import check_new_zamena
from data.schedule_api import ScheduleApi
from my_secrets import (
    CHECK_ZAMENA_INTERVAL_START_HOUR,
    CHECK_ZAMENA_INTERVAL_END_HOUR,
    CHECK_ZAMENA_INTERVAL_MINUTES,
    API_KEY,
    API_URL,
    TOKEN,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

dp = Dispatcher(api=ScheduleApi(api_key=API_KEY, api_url=API_URL))
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("aiohttp").setLevel(logging.DEBUG)
    scheduler = AsyncIOScheduler()

    if CHECK_ZAMENA_INTERVAL_MINUTES is not None:
        trigger = CronTrigger(
            minute=f"0/{CHECK_ZAMENA_INTERVAL_MINUTES}",
            hour=f"{CHECK_ZAMENA_INTERVAL_START_HOUR}-{CHECK_ZAMENA_INTERVAL_END_HOUR}",
            timezone="Asia/Yekaterinburg",
            jitter=180,
        )
        scheduler.add_job(check_new_zamena, trigger, args=(bot,))
    scheduler.start()

    dp.include_routers(
        navigation.router,
        search.router,
        test.router,
        parser.router,
        events.router,
        notifications.router,
    )
    try:
        await on_on()
        await dp.start_polling(bot)
        await check_new_zamena(bot=bot)
    finally:
        scheduler.shutdown()
        await on_exit(bot=bot)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
