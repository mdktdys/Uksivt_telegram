import asyncio
import logging
import sys

from src.modules.auth.auth_router import router as auth_router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from callbacks import navigation, search, parser, events, notifications, queues_router, menu_router, settings_router
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
from src.middlewares.services_middleware import ServicesMiddleware
from src.services.data_service import DataService
from src.services.assets_service import AssetsService
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.router import router

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
        router,
        navigation.router,
        search.router,
        auth_router,
        parser.router,
        events.router,
        queues_router.router,
        menu_router.router,
        settings_router.router,
        notifications.router,
    )
    
    data_service: DataService = DataService()
    assets_service: AssetsService = AssetsService()
    services_middleware: ServicesMiddleware = ServicesMiddleware(data_service, assets_service)
    dp.message.middleware(services_middleware)
    dp.callback_query.middleware(services_middleware)

    try:
        await on_on(bot = bot)
        await dp.start_polling(bot)
        await check_new_zamena(bot = bot)
    finally:
        scheduler.shutdown()
        await on_exit(bot=bot)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
