import os
import re
import logging
import time
from typing import Any, AsyncIterator, Iterator

from aiogram.types import Message
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from llama_cpp import Llama


logger = logging.getLogger(__name__)


class TextPipeline:
    opening_thinking_tags = ['<think>', '&lt;think&gt;']
    closing_thinking_tags = ['</think>', '&lt;/think&gt;']
    all_thinking_tags = [*opening_thinking_tags, *closing_thinking_tags]

    @staticmethod
    def is_support_system_role(chat_template: str):
        return 'System role not supported' not in chat_template

    @classmethod
    def clean_thinking_tags(cls, text: str) -> str:
        for open_tag, close_tag in zip(cls.opening_thinking_tags, cls.closing_thinking_tags):
            pattern = rf'{open_tag}.*?{close_tag}'
            text = re.sub(pattern, '', text, flags=re.DOTALL)
        return text

    @staticmethod
    def transliterate_english_to_russian(text: str) -> str:
        translit_map = {
            'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е',
            'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'ж',
            'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
            'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т',
            'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'й',
            'z': 'з',
            'A': 'А', 'B': 'Б', 'C': 'К', 'D': 'Д', 'E': 'Е',
            'F': 'Ф', 'G': 'Г', 'H': 'Х', 'I': 'И', 'J': 'Ж',
            'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О',
            'P': 'П', 'Q': 'К', 'R': 'Р', 'S': 'С', 'T': 'Т',
            'U': 'У', 'V': 'В', 'W': 'В', 'X': 'КС', 'Y': 'Й',
            'Z': 'З',
            '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
            '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять',
            '+': ' плюс ', '-': ' минус ', '=': ' равно ',
            '*': ' умножить ', '/': ' разделить ', '%': ' процент ',
        }
        
        def transliterate_char(char):
            return translit_map.get(char, char)
        
        return ''.join(transliterate_char(c) for c in text)
        
    @classmethod
    def clean_text_before_speech(cls, text: str) -> str:
        text = cls.clean_thinking_tags(text)
        text = cls.transliterate_english_to_russian(text)
        text = re.sub(r"[^a-zA-Zа-яА-Я0-9\s.,!?;:()\"'-]", '', text)
        text = re.sub(r'[\"\'«»]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def _prepare_messages(
        system_prompt: str,
        support_system_role: bool,
        user_message: str,
    ) -> list[dict[str, str]]:
        messages = []
        if support_system_role and system_prompt:
            messages.append(dict(role='system', content=system_prompt))
        messages.append(dict(role='user', content=user_message))
        return messages

    @classmethod
    def generate_from_chat_completion(
        cls,
        model: Llama,
        tokenizer: PreTrainedTokenizerBase | None,
        system_prompt: str,
        user_message_text: str,
        enable_thinking: bool,
        generation_kwargs: dict[str, Any],
    ) -> Iterator[str]:
        logging.debug(f'LLM response generation started, process PID: {os.getpid()}')
        support_system_role = cls.is_support_system_role(model.metadata['tokenizer.chat_template'])
        messages = cls._prepare_messages(
            system_prompt=system_prompt,
            support_system_role=support_system_role,
            user_message=user_message_text,
        )
        if tokenizer:
            formatted_prompt = tokenizer.apply_chat_template(
                conversation=messages,
                add_generation_prompt=True,
                tokenize=False,
                enable_thinking=enable_thinking,
            )
            stream_response = model.create_completion(
                prompt=formatted_prompt,
                stream=True,
                stop=[tokenizer.eos_token],
                **generation_kwargs,
            )
            for chunk in stream_response:
                token = chunk['choices'][0].get('text')
                if token is not None:
                    yield token
        else:
            stream_response = model.create_chat_completion(
                messages=messages,
                stream=True,
                **generation_kwargs,
            )
            for chunk in stream_response:
                token = chunk['choices'][0]['delta'].get('content')
                if token is not None:
                    yield token

    @classmethod
    def get_llm_response(
        cls,
        generator: Iterator[str],
        show_thinking: bool,
    ) -> str:
        response_text = ''
        for i, token in enumerate(generator):
            response_text += token
        if not show_thinking:
            response_text = cls.clean_thinking_tags(response_text)
        return response_text

    @classmethod
    async def astream_llm_response(
        cls,
        generator: AsyncIterator[str],
        show_thinking: bool,
    ) -> AsyncIterator[str]:
        response_text = ''
        is_think = False
        async for token in generator:
            if show_thinking:
                response_text += token
            else:
                if token in cls.opening_thinking_tags:
                    is_think = True
                    response_text = 'Thinking...'
                elif token in cls.closing_thinking_tags:
                    is_think = False
                    response_text = ''
                if not is_think and token not in cls.closing_thinking_tags:
                    response_text += token
            yield response_text

    @classmethod
    async def astream_llm_response_to_aiogram_bot(
        cls,
        generator: AsyncIterator[str],
        bot_message: Message,
        show_thinking: bool,
    ) -> str:
        editing_frequency = 1
        response_message_text = ''
        response_message = bot_message
        last_edit_time = time.monotonic()
        async for response_text in cls.astream_llm_response(generator=generator, show_thinking=show_thinking):
            if not response_text.strip() or (response_text.strip() == response_message_text.strip()):
                continue
            now = time.monotonic()
            if now - last_edit_time < editing_frequency:
                continue
            # with suppress(TelegramBadRequest):
            response_message = await bot_message.edit_text(text=response_text)
            response_message_text = response_message.text
            last_edit_time = now
        if response_text.strip() and (response_text.strip() != response_message_text.strip()):
            # with suppress(TelegramBadRequest):
            await response_message.edit_text(text=response_text)
        return response_text
