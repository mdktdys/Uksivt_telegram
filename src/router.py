from aiogram import Router

from .modules.misc.misc_router import router as misc_router
from .modules.timings.timings_router import router as timings_router

router = Router(name = 'main_router')

router.include_router(timings_router)
router.include_router(misc_router)