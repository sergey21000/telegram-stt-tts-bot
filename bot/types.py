from typing import Any
from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import Message

from llama_cpp import Llama
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

from vosk_tts import Model as Synth
from vosk import Model as KaldiRecognizer

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


@dataclass
class Models:
    model_llm: Llama
    tokenizer: PreTrainedTokenizerBase | None
    synth_tts: Synth
    recognizer_stt: KaldiRecognizer
