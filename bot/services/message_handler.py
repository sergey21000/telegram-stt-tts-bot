import asyncio
import base64
import tempfile
import time
from typing import AsyncIterator
from pathlib import Path

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import FSInputFile

from chatgpt_md_converter import telegram_format
import speech_recognition as sr
from loguru import logger

from bot.texts.locales.ru import Texts
from bot.services.text import TextPipeline
from bot.services.speech import SpeechPipeline
from bot.init.models import llm_client, stt_recognizer

from config.config import Config
from config.user import UserConfig
from config.queue import QueueConfig


class MessageHandler:
    @classmethod
    async def speech_to_speech_answer_handler(
        cls,
        user_message: Message,
        bot_message: Message,
        bot: Bot,
        texts: Texts,
        user_config: UserConfig,
        position: int,
    ) -> None:
        status_text = texts.ProcessMessages.wait_bot_answer_with_position(
            position=position,
            n_max_concurrent_tasks=QueueConfig.N_MAX_CONCURRENT_TASKS_IN_QUEUE,
        )
        await bot_message.edit_text(
            text=status_text,
            disable_notification=True,
            parse_mode='HTML',
        )
        disable_notification = user_config.answer_with_voice
        # audio or video
        if (user_message.audio or user_message.video) and not user_message.text:
            async with ChatActionSender(bot=bot, chat_id=user_message.from_user.id, action='typing'):
                status_text += texts.ProcessMessages.convert_media_to_wav + '\n'
                await bot_message.edit_text(
                    text=status_text,
                    disable_notification=True,
                    parse_mode='HTML',
                )
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
                    wav_path = tmp_wav.name
                file_obj = user_message.audio or user_message.video
                await bot.download(file_obj, destination=wav_path + '_source')
                convert_ok = await asyncio.to_thread(
                    SpeechPipeline.convert_media_to_wav,
                    input_file=wav_path + '_source',
                    output_file=wav_path,
                    sample_rate=Config.SAMPLE_RATE_BEFORE_STT,
                )
                if not convert_ok:
                    await user_message.answer(texts.ProcessMessages.convert_media_to_wav_error)
                    return
                status_text += texts.ProcessMessages.tts + '\n'
                await bot_message.edit_text(
                    text=status_text,
                    disable_notification=True,
                    parse_mode='HTML',
                )
                user_message_text = await asyncio.to_thread(
                    SpeechPipeline.speech_to_text,
                    stt_recognizer=stt_recognizer,
                    wav_audio_path=wav_path,
                )
                logger.debug(f'Recognized text from audio/video: {user_message_text}')
                Path(wav_path + '_source').unlink(missing_ok=True)
                Path(wav_path).unlink(missing_ok=True)
                await user_message.answer(
                    text=user_message_text,
                    disable_notification=False,
                    parse_mode='HTML',
                )
                return

        # text or (photo and text)
        user_message_text = user_message.caption or user_message.text
        image = user_message.photo[-1] if user_message.photo else None
        image_base64 = None
        if image:
            file = await bot.get_file(image.file_id)
            image_bytes = await bot.download_file(file.file_path)
            image_base64 = base64.b64encode(image_bytes.read()).decode()

        if user_message.voice:
            async with ChatActionSender(bot=bot, chat_id=user_message.from_user.id, action='typing'):
                status_text += texts.ProcessMessages.convert_media_to_wav + '\n'
                await bot_message.edit_text(
                    text=status_text,
                    disable_notification=True,
                    parse_mode='HTML',
                )
                with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as tmp_ogg, \
                    tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
                    ogg_voice_name = tmp_ogg.name
                    wav_voice_name = tmp_wav.name
                await bot.download(user_message.voice, destination=ogg_voice_name)
                convert_is_ok = await asyncio.to_thread(
                    SpeechPipeline.convert_media_to_wav,
                    input_file=ogg_voice_name,
                    output_file=wav_voice_name,
                    sample_rate=Config.SAMPLE_RATE_BEFORE_STT,
                )
                if not convert_is_ok:
                    await user_message.answer(texts.ProcessMessages.convert_media_to_wav_error)
                    return
                status_text += texts.ProcessMessages.stt + '\n'
                await bot_message.edit_text(
                    text=status_text,
                    disable_notification=True,
                    parse_mode='HTML',
                )
                user_message_text = await asyncio.to_thread(
                    SpeechPipeline.speech_to_text,
                    stt_recognizer=stt_recognizer,
                    wav_audio_path=wav_voice_name,
                )
                logger.debug(f'Recognized text from voice: {user_message_text}')
                Path(ogg_voice_name).unlink(missing_ok=True)
                Path(wav_voice_name).unlink(missing_ok=True)

        if not user_message_text:
            await user_message.answer(texts.ProcessMessages.speech_recognition_error)
            return
        # get llm response
        agenerator = llm_client.astream(
            user_message_or_messages=user_message_text,
            image_path_or_base64=image_base64,
            resize_size=Config.IMAGE_RESIZE_SIZE,
            completions_kwargs=user_config.get_completions_kwargs(),
            show_thinking=user_config.show_thinking,
            return_per_token=True,
            out_token_in_thinking_mode='Thinking ...',
        )
        async with ChatActionSender(bot=bot, chat_id=user_message.from_user.id, action='typing'):
            status_text += texts.ProcessMessages.llm + '\n'
            await bot_message.edit_text(
                text=status_text,
                disable_notification=True,
                parse_mode='HTML',
            )
            if user_config.stream_llm_response and user_config.answer_with_text:
                # stream llm response
                response_text = await cls.astream_llm_response_to_aiogram_bot(
                    agenerator=agenerator,
                    bot_message=bot_message,
                )
            else:
                # answer llm response
                response_text = ''
                async for text in agenerator:
                    response_text += text
                logger.debug(f'Raw response text from llm: {response_text}')
                if not user_config.show_thinking:
                    response_text = TextPipeline.clean_thinking_tags(response_text)
                    logger.debug(f'Text from llm after clean: {response_text}')
                # response_text = response_text[:Config.MAX_N_CHARS_IN_MESSAGE]
                if user_config.answer_with_text:
                    response_text_for_edit = telegram_format(response_text)
                    logger.debug(f'Text from llm after telegram_format: {response_text_for_edit}')
                    logger.debug(f'len text before bot_message.edit_text: {len(response_text_for_edit)}')
                    await user_message.answer(
                        text=response_text_for_edit,
                        disable_notification=disable_notification,
                        parse_mode='HTML',
                    )
        # tts
        if user_config.answer_with_voice:
            async with ChatActionSender(bot=bot, chat_id=user_message.from_user.id, action='record_voice'):
                if Config.MAX_N_CHARS_BEFORE_TTS:
                    response_text = response_text[:Config.MAX_N_CHARS_BEFORE_TTS]
                status_text += texts.ProcessMessages.tts + '\n'
                await bot_message.edit_text(
                    text=status_text,
                    disable_notification=True,
                    parse_mode='HTML',
                )
                response_text = TextPipeline.clean_text_before_edge_tts(response_text)
                logger.debug(f'len text before tts: {len(response_text)}')
                logger.debug(f'Text before tts: {response_text}')
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_tts:
                    tts_audio_path = tmp_tts.name
                await SpeechPipeline.text_to_speech(
                    text=response_text,
                    voice=user_config.voice,
                    tts_audio_path=tts_audio_path,
                )
                audio_file = FSInputFile(tts_audio_path)
                await user_message.answer_voice(voice=audio_file)
                Path(tts_audio_path).unlink(missing_ok=True)


    @staticmethod
    async def astream_llm_response_to_aiogram_bot(
        agenerator: AsyncIterator[str],
        bot_message: Message,
    ) -> str:
        editing_frequency_seconds = 1
        full_response_text = ''
        displayed_text  = ''
        response_message = bot_message
        last_edit_time = time.monotonic()
        async for token in agenerator:
            full_response_text += token
            if not full_response_text.strip() or (full_response_text.strip() == displayed_text.strip()):
                continue
            if len(full_response_text) >= 4096:
                return full_response_text
            now = time.monotonic()
            if now - last_edit_time < editing_frequency_seconds:
                continue
            # with suppress(TelegramBadRequest):
            response_message = await bot_message.edit_text(text=full_response_text)
            displayed_text = response_message.text
            last_edit_time = now
        if full_response_text.strip() and (full_response_text.strip() != displayed_text.strip()):
            # with suppress(TelegramBadRequest):
            await response_message.edit_text(text=full_response_text)
        return full_response_text
