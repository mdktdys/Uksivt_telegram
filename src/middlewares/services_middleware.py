from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import TelegramObject
from src.services.data_service import DataService


class ServicesMiddleware(BaseMiddleware):
    def __init__(self, data_service: DataService) -> None:
        super().__init__()
        self.data_service: DataService = data_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["data_service"] = self.data_service
        return await handler(event, data)
