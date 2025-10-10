from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.database.user_db import DataBase


class DbMiddleware(BaseMiddleware):
    def __init__(self, db: DataBase):
        super().__init__()
        self.db = db

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data['db'] = self.db
        return await handler(event, data)
