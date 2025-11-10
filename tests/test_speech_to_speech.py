import os
import wave
from pathlib import Path

from colorama import Fore, Style

from bot.types import Models
from bot.services.llm import TextPipeline
from bot.services.speech import SpeechPipeline

from config.config import Config
from config.user import UserConfig


def test_speech_to_speech(models: Models, user_config: UserConfig, text_with_thinking: str):
    ogg_voice_path = Path('tests/test_files/audio_with_speech.ogg')
    wav_voice_path = Path('tests/test_files/audio_with_speech.wav')
    wav_voice_path.unlink(missing_ok=True)
    
    convert_is_ok = SpeechPipeline.convert_ogg_to_wav(
        input_file=ogg_voice_path,
        output_file=wav_voice_path,
        sample_rate=Config.SAMPLE_RATE,
    )
    
    assert convert_is_ok, 'Error converting ogg to wav'
    sst_text = SpeechPipeline.speech_to_text(
        recognizer=models.recognizer_stt,
        wav_audio_path=str(wav_voice_path),
    )
    print()
    print(f'{Fore.YELLOW}{Style.BRIGHT}SST text:{Style.RESET_ALL}\n{sst_text}')
    
    assert isinstance(sst_text, str), 'SST text is not a string'
    assert 165 < len(sst_text) < 170, 'SST text contains more or fewer characters than the audio'
    wav_voice_path.unlink(missing_ok=True)
    
    generator = TextPipeline.generate_from_chat_completion(
        model=models.model_llm,
        tokenizer=models.tokenizer,
        system_prompt=user_config.system_prompt,
        user_message_text=sst_text,
        enable_thinking=user_config.enable_thinking,
        generation_kwargs=user_config.get_generation_kwargs(),
    )
    llm_text = TextPipeline.get_llm_response(
        generator=generator,
        show_thinking=user_config.show_thinking,
    )
    
    llm_text = text_with_thinking + llm_text
    print(f'{Fore.RED}{Style.BRIGHT}LLM text before cleaning:{Style.RESET_ALL}\n{llm_text}')
    llm_text = TextPipeline.clean_text_before_speech(text=llm_text)
    print(f'{Fore.GREEN}{Style.BRIGHT}LLM text after cleaning:{Style.RESET_ALL}\n{llm_text}')
    
    assert all([
        tag not in llm_text for tag in TextPipeline.all_thinking_tags
    ]), 'The thought tags before the TTS were not removed'
    
    speaker_id = Config.VOICE_NAME_TO_IDX[user_config.voice_name]
    tts_audio_path = Path(
        os.getenv('TTS_AUDIO_DIR', 'tests/test_files/')
    ) / f'tts_result_voice_{sst_text[:6]}.wav'
    tts_audio_path.unlink(missing_ok=True)
    
    SpeechPipeline.text_to_speech(
        synth_tts=models.synth_tts,
        text=llm_text,
        speaker_id=speaker_id,
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
