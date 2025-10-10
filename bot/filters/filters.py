from aiogram.types import Message
from config.config import Config


class Filters:
    @staticmethod
    async def admin_filter(message: Message) -> bool:
        if Config.ADMIN_CHAT_ID:
            return message.from_user.id == int(Config.ADMIN_CHAT_ID)
        return True
