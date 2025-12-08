from typing import Any
from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import Message

from bot.texts.locales.ru import Texts
from config.user import UserConfig


@dataclass
class SpeechToSpeechQueueKwargs:
    user_message: Message
    bot_message: Message
    bot: Bot
    texts: Texts
    user_config: UserConfig

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
