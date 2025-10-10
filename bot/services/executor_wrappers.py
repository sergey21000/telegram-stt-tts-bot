import asyncio
import multiprocessing
import concurrent.futures
from typing import Any

from aiogram.types import Message

from bot.services.llm import TextPipeline
from bot.services.speech import SpeechPipeline
from bot.init.worker_models import get_worker_models


class PipelineExecutorWrapper:
    def get_generator_from_completion_wrapper(
        system_prompt: str,
        user_message_text: str,
        enable_thinking: bool,
        generation_kwargs: dict[str, Any],
    ):
        MODELS = get_worker_models()
        return TextPipeline.generate_from_chat_completion(
            model=MODELS.model_llm,
            tokenizer=MODELS.tokenizer,
            system_prompt=system_prompt,
            user_message_text=user_message_text,
            enable_thinking=enable_thinking,
            generation_kwargs=generation_kwargs,
        )

    @classmethod
    def get_llm_response_executor_wrapper(
        cls,
        system_prompt: str,
        user_message_text: str,
        enable_thinking: bool,
        generation_kwargs: dict[str, Any],
        show_thinking: bool,
    ) -> str:
        generator = cls.get_generator_from_completion_wrapper(
            system_prompt=system_prompt,
            user_message_text=user_message_text,
            enable_thinking=enable_thinking,
            generation_kwargs=generation_kwargs,
        )
        return TextPipeline.get_llm_response(
            generator=generator,
            show_thinking=show_thinking,
        )

    @classmethod
    def _generate_and_stream(
        cls,
        queue: multiprocessing.Queue,
        system_prompt: str,
        user_message_text: str,
        enable_thinking: bool,
        generation_kwargs: dict[str, Any],
    ):
        generator = cls.get_generator_from_completion_wrapper(
            system_prompt=system_prompt,
            user_message_text=user_message_text,
            enable_thinking=enable_thinking,
            generation_kwargs=generation_kwargs,
        )
        for chunk in generator:
            queue.put(chunk)
        queue.put(None)

    @staticmethod
    async def astream_from_queue(queue: multiprocessing.Queue, pool: concurrent.futures.Executor):
        loop = asyncio.get_running_loop()
        while True:
            chunk = await loop.run_in_executor(pool, queue.get)
            if chunk is None:
                break
            yield chunk

    @classmethod
    async def astream_llm_response_to_aiogram_bot_wrapper(
        cls,
        pool: concurrent.futures.Executor,
        bot_message: Message,
        system_prompt: str,
        user_message_text: str,
        enable_thinking: bool,
        generation_kwargs: dict[str, Any],
        show_thinking: bool,
    ):
        with multiprocessing.Manager() as manager:
            queue = manager.Queue()
            future = pool.submit(
                cls._generate_and_stream,
                queue,
                system_prompt,
                user_message_text,
                enable_thinking,
                generation_kwargs,
            )
            async_generator = cls.astream_from_queue(queue=queue, pool=pool)
            response_text = await TextPipeline.astream_llm_response_to_aiogram_bot(
                generator=async_generator,
                bot_message=bot_message,
                show_thinking=show_thinking,
            )
            future.result()
            return response_text
        
    @staticmethod
    def text_to_speech_wrapper(
        text: str,
        speaker_id: int,
        tts_audio_path: str,
    ) -> None:
        MODELS = get_worker_models()
        return SpeechPipeline.text_to_speech(
            synth_tts=MODELS.synth_tts,
            text=text,
            speaker_id=speaker_id,
            tts_audio_path=tts_audio_path,
        )

    @staticmethod
    def speech_to_text_wrapper(wav_audio_path: str) -> None:
        MODELS = get_worker_models()
        return SpeechPipeline.speech_to_text(
            recognizer=MODELS.recognizer_stt,
            wav_audio_path=wav_audio_path,
        )
