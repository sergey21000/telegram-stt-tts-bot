import os
import wave
from pathlib import Path

import pytest
from colorama import Fore, Style
from llama_cpp_py import LlamaAsyncClient

from bot.services.text import TextPipeline
from bot.services.speech import SpeechPipeline

from config.config import Config
from config.user import UserConfig


@pytest.mark.asyncio
@pytest.mark.parametrize('text', [
    'Кто ты и что ты умеешь?',
    'Почему трава зеленая?',
    'Сколько будет 2 + 2?',
])
async def test_text_to_speech(llm_client: LlamaAsyncClient, user_config: UserConfig, text: str):
    agenerator = llm_client.astream(
        user_message_or_messages=text,
        image_path_or_base64=None,
        resize_size=Config.IMAGE_RESIZE_SIZE,
        completions_kwargs=user_config.get_completions_kwargs(),
        show_thinking=user_config.show_thinking,
        return_per_token=True,
        out_token_in_thinking_mode='Thinking ...',
    )
    llm_text = ''
    async for text in agenerator:
        llm_text += text
    
    print(f'\n{Fore.RED}{Style.BRIGHT}LLM text before cleaning:{Style.RESET_ALL}\n{llm_text}')
    llm_text = TextPipeline.clean_text_before_edge_tts(text=llm_text)
    print(f'\n{Fore.GREEN}{Style.BRIGHT}LLM text after cleaning:{Style.RESET_ALL}\n{llm_text}')
    
    assert all([
        tag not in llm_text for tag in TextPipeline.all_thinking_tags
    ]), 'The thought tags before the TTS were not removed'
    

    tts_audio_path = Path(
        os.getenv('TTS_AUDIO_DIR', 'tests/test_files/')
    ) / f'tts_result_voice_{text[:6]}.wav'
    tts_audio_path.unlink(missing_ok=True)
    
    await SpeechPipeline.text_to_speech(
        text=llm_text,
        voice=user_config.voice,
        tts_audio_path=str(tts_audio_path),
    )
    assert tts_audio_path.exists(), 'TTS audio file was not created'
    assert tts_audio_path.stat().st_size > 44, 'WAV file too small — maybe invalid'

    with wave.open(str(tts_audio_path), 'rb') as wf:
        n_channels = wf.getnchannels()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()

    assert n_channels in (1, 2), f'Unexpected number of channels: {n_channels}'
    assert framerate > 0, 'Invalid sample rate'
    assert n_frames > 0, 'Empty WAV file'

    file_size_kb = tts_audio_path.stat().st_size / 1024
    print(f'{Fore.CYAN}TTS Audio created: {tts_audio_path} ({file_size_kb:.1f} KB){Style.RESET_ALL}')
