import subprocess
import logging
import wave
import json

from config import SAMPLE_RATE
from infer_models import recognizer, model, SUPPORT_SYSTEM_ROLE, synth


logger = logging.getLogger(__name__)

def speech_to_text(audio_path: str) -> str:
    wf = wave.open(audio_path, 'rb')
    audio_data = wf.readframes(-1)
    sample_rate = wf.getframerate()
    recognizer.AcceptWaveform(audio_data)
    recognize_text = json.loads(recognizer.FinalResult())['text']
    return recognize_text


def text_to_text(user_message: str, system_prompt:str, generation_kwargs: dict):
    messages = []
    if system_prompt and SUPPORT_SYSTEM_ROLE:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_message})
    response = model.create_chat_completion(
        messages=messages,
        **generation_kwargs,
        )
    generated_text = response['choices'][0]['message']['content']
    return generated_text


def text_to_speech(generated_text: str, speaker_index: int)-> str:
    audio_path_tts = 'input_voice.wav'
    synth.synth(generated_text, audio_path_tts, speaker_id=speaker_index)
    return audio_path_tts


def convert_ogg_to_wav(input_file: str, output_file: str):
    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', input_file, '-ar', str(SAMPLE_RATE), output_file],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as ex:
        logger.error(f'Ошибка при конвертации ogg в wav:\n{ex} \nСообщение ошибки: \n{ex.stderr}')
        return False
