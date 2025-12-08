import os

from aiogram.types import Message
from aiogram.utils.magic_filter import MagicFilter
from aiogram import F

from config.config import Config


class Filters:
    @staticmethod
    async def is_admin(message: Message) -> bool:
        if Config.ADMIN_CHAT_ID:
            return message.from_user.id == int(Config.ADMIN_CHAT_ID)
        return True

    async def is_support_photo(message: Message) -> MagicFilter:
        if os.getenv('LLAMA_ARG_MMPROJ') or os.getenv('LLAMA_ARG_MMPROJ_URL'):
            return (F.text & ~F.text.startswith('/')) | F.voice | F.photo
        return (F.text & ~F.text.startswith('/')) | F.voice