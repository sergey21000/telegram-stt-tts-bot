from typing import Callable

from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class BotMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(self, handler: Callable, event: Message, data: dict):
        data['bot'] = self.bot
        return await handler(event, data)
