from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.database.user_db import DataBase
from bot.texts.localization import Localization
from bot.texts.locales.ru import Texts


class TextsByLangMiddleware(BaseMiddleware):
    def __init__(self, db: DataBase):
        super().__init__()
        self.db = db

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_id: int = event.from_user.id
        user_lang: str | None = await self.db.get_user_lang(user_id)
        texts: Texts = Localization.get_texts_by_lang(lang=user_lang)
        data['texts'] = texts
        return await handler(event, data)
