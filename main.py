import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from callbacks import (
    events,
    menu_router,
    navigation,
    notifications,
    parser,
    queues_router,
    search,
    settings_router,
)
from callbacks.events import on_exit, on_on
from core.methods import check_new_zamena
from data.schedule_api import ScheduleApi
from my_secrets import (
    API_KEY,
    API_URL,
    CHECK_ZAMENA_INTERVAL_END_HOUR,
    CHECK_ZAMENA_INTERVAL_MINUTES,
    CHECK_ZAMENA_INTERVAL_START_HOUR,
    TOKEN,
)
from src.middlewares.services_middleware import ServicesMiddleware
from src.middlewares.user_middleware import UserMiddleware
from src.modules.auth.auth_router import router as auth_router
from src.modules.tests.test_router import router as test_router
from src.router import router
from src.services.assets_service import AssetsService
from src.services.data_service import DataService
from src.services.user_service import UserService
from utils.logger import logger

logger.info('as')

logger.info('🚀 Бот запускается')
dp = Dispatcher(api = ScheduleApi(api_key = API_KEY, api_url = API_URL))
bot = Bot(token = TOKEN, default = DefaultBotProperties(parse_mode = ParseMode.HTML))
logger.info('⚙️ Бот запущен')

async def main() -> None:
    scheduler = AsyncIOScheduler()

    # if CHECK_ZAMENA_INTERVAL_MINUTES is not None:
    #     trigger = CronTrigger(
    #         minute=f"0/{CHECK_ZAMENA_INTERVAL_MINUTES}",
    #         hour=f"{CHECK_ZAMENA_INTERVAL_START_HOUR}-{CHECK_ZAMENA_INTERVAL_END_HOUR}",
    #         timezone="Asia/Yekaterinburg",
    #         jitter=180,
    #     )
    #     scheduler.add_job(check_new_zamena, trigger, args=(bot,))
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
        test_router
    )
    logger.info('⚙️ Добавлены роутеры')
    
    data_service: DataService = DataService()
    assets_service: AssetsService = AssetsService()

    services_middleware: ServicesMiddleware = ServicesMiddleware(data_service, assets_service)
    dp.message.middleware(services_middleware)
    dp.callback_query.middleware(services_middleware)
    
    user_service: UserService = UserService()
    user_middleware: UserMiddleware = UserMiddleware(user_service)
    dp.message.middleware(user_middleware)
    dp.callback_query.middleware(user_middleware)

    try:
        await on_on(bot = bot)
        await dp.start_polling(bot)
        await check_new_zamena(bot = bot)
    finally:
        scheduler.shutdown()
        await on_exit(bot = bot)


if __name__ == "__main__":
    logger.info('Запуск')

    asyncio.run(main())