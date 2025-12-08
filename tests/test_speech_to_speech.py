import asyncio
import os
import wave
from pathlib import Path

import pytest
from colorama import Fore, Style
from llama_cpp_py import LlamaAsyncClient
import speech_recognition as sr

from bot.services.text import TextPipeline
from bot.services.speech import SpeechPipeline

from config.config import Config
from config.user import UserConfig


@pytest.mark.asyncio
async def test_speech_to_speech(
    llm_client: LlamaAsyncClient,
    user_config: UserConfig,
    text_with_thinking: str,
):
    ogg_voice_path = Path('tests/test_files/audio_with_speech.ogg')
    wav_voice_path = Path('tests/test_files/audio_with_speech.wav')
    wav_voice_path.unlink(missing_ok=True)
    
    convert_is_ok = await asyncio.to_thread(
        SpeechPipeline.convert_media_to_wav,
        input_file=ogg_voice_path,
        output_file=wav_voice_path,
        sample_rate=Config.SAMPLE_RATE_BEFORE_STT,
    )
    
    assert convert_is_ok, 'Error converting ogg to wav'

    stt_recognizer = sr.Recognizer()
    sst_text = await asyncio.to_thread(
        SpeechPipeline.speech_to_text,
        stt_recognizer=stt_recognizer,
        wav_audio_path=str(wav_voice_path),
    )
    print()
    print(f'\n{Fore.YELLOW}{Style.BRIGHT}SST text:{Style.RESET_ALL}\n{sst_text}')
    
    assert isinstance(sst_text, str), 'SST text is not a string'
    assert 165 < len(sst_text) < 170, 'SST text contains more or fewer characters than the audio'
    wav_voice_path.unlink(missing_ok=True)

    agenerator = llm_client.astream(
        user_message_or_messages=sst_text,
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
    
    llm_text = text_with_thinking + llm_text
    print(f'\n{Fore.RED}{Style.BRIGHT}LLM text before cleaning:{Style.RESET_ALL}\n{llm_text}')
    llm_text = TextPipeline.clean_text_before_edge_tts(text=llm_text)
    print(f'\n{Fore.GREEN}{Style.BRIGHT}LLM text after cleaning:{Style.RESET_ALL}\n{llm_text}')
    
    assert all([
        tag not in llm_text for tag in TextPipeline.all_thinking_tags
    ]), 'The thought tags before the TTS were not removed'
    
    tts_audio_path = Path(
        os.getenv('TTS_AUDIO_DIR', 'tests/test_files/')
    ) / f'tts_result_voice_{sst_text[:6]}.wav'
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
