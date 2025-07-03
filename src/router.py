from aiogram import Router
from .modules.timings.timings_router import router as timings_router

router = Router(name = 'main_router')

router.include_router(timings_router)