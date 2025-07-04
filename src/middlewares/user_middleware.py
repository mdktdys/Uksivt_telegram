from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.services.user_service import UserService
from models.user_model import User

class UserMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service: UserService = user_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if hasattr(event, 'from_user') and event.from_user:
            user: User = await self.user_service.get_user(user_id = event.from_user.id)

            data['user'] = user
            data['user_service'] = self.user_service

        return await handler(event, data)