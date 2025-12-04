import asyncio
import concurrent
import functools
import tempfile
from pathlib import Path

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import FSInputFile
from chatgpt_md_converter import telegram_format

from bot.services.executor_wrappers import PipelineExecutorWrapper
from bot.texts.locales.ru import Texts
from bot.services.llm import TextPipeline
from bot.services.speech import SpeechPipeline

from config.config import Config
from config.user import UserConfig


async def speech_to_speech_answer_handler(
    user_message: Message,
    bot_message: Message,
    bot: Bot,
    texts: Texts,
    user_config: UserConfig,
    pool: concurrent.futures.ProcessPoolExecutor,
) -> None:
    user_message_text = user_message.text
    loop = asyncio.get_running_loop()
    if user_message.voice:
        async with ChatActionSender(bot=bot, chat_id=user_message.from_user.id, action='typing'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as tmp_ogg, \
                tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
                ogg_voice_name = tmp_ogg.name
                wav_voice_name = tmp_wav.name
            await bot.download(user_message.voice, destination=ogg_voice_name)
            convert_is_ok = await loop.run_in_executor(pool, functools.partial(
                SpeechPipeline.convert_ogg_to_wav,
                input_file=ogg_voice_name,
                output_file=wav_voice_name,
                sample_rate=Config.SAMPLE_RATE,
            ))
            if not convert_is_ok:
                await user_message.answer(texts.ProcessMessages.convert_ogg_to_wav_error)
                return
            user_message_text = await loop.run_in_executor(pool, functools.partial(
                PipelineExecutorWrapper.speech_to_text_wrapper,
                wav_audio_path=wav_voice_name,
            ))
            Path(ogg_voice_name).unlink(missing_ok=True)
            Path(wav_voice_name).unlink(missing_ok=True)
    if not user_message_text:
        await user_message.answer(texts.ProcessMessages.speech_recognition_error)
        return
    async with ChatActionSender(bot=bot, chat_id=user_message.from_user.id, action='typing'):
        disable_notification = user_config.answer_with_voice
        if user_config.stream_llm_response and user_config.answer_with_text:
            response_text = await PipelineExecutorWrapper.astream_llm_response_to_aiogram_bot_wrapper(
                pool=pool,
                bot_message=bot_message,
                system_prompt=user_config.system_prompt,
                user_message_text=user_message_text,
                enable_thinking=user_config.enable_thinking,
                generation_kwargs=user_config.get_generation_kwargs(),
                show_thinking=user_config.show_thinking,
            )
        else:
            response_text = await loop.run_in_executor(pool, functools.partial(
                PipelineExecutorWrapper.get_llm_response_executor_wrapper,
                system_prompt=user_config.system_prompt,
                user_message_text=user_message_text,
                enable_thinking=user_config.enable_thinking,
                generation_kwargs=user_config.get_generation_kwargs(),
                show_thinking=user_config.show_thinking,
            ))
            response_text = response_text[:Config.MAX_N_CHARS_IN_MESSAGE]
            if user_config.answer_with_text:
                response_text = telegram_format(response_text)
                await bot_message.edit_text(
                    text=response_text,
                    disable_notification=disable_notification,
                )
    if user_config.answer_with_voice:
        async with ChatActionSender(bot=bot, chat_id=user_message.from_user.id, action='record_voice'):
            speaker_id = Config.VOICE_NAME_TO_IDX[user_config.voice_name]
            response_text = TextPipeline.clean_text_before_speech(text=response_text)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_tts:
                tts_audio_path = tmp_tts.name
            await loop.run_in_executor(pool, functools.partial(
                PipelineExecutorWrapper.text_to_speech_wrapper,
                text=response_text,
                speaker_id=speaker_id,
                tts_audio_path=tts_audio_path,
            ))
            audio_file = FSInputFile(tts_audio_path)
            await user_message.answer_voice(voice=audio_file)
            Path(tts_audio_path).unlink(missing_ok=True)
