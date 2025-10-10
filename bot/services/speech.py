import logging
import subprocess
import json

import wave
from vosk_tts import Model as Synth
from vosk import Model as KaldiRecognizer


logger = logging.getLogger(__name__)


class SpeechPipeline:
    @staticmethod
    def speech_to_text(recognizer: KaldiRecognizer, wav_audio_path: str) -> str:
        with wave.open(wav_audio_path, 'rb') as wf:
            audio_data = wf.readframes(-1)
        recognizer.AcceptWaveform(audio_data)
        recognized_text = json.loads(recognizer.FinalResult())['text']
        return recognized_text

    @staticmethod
    def text_to_speech(synth_tts: Synth, text: str, speaker_id: int, tts_audio_path: str) -> None:
        synth_tts.synth(text=text, oname=tts_audio_path, speaker_id=speaker_id)

    @staticmethod
    def convert_ogg_to_wav(input_file: str, output_file: str, sample_rate: int) -> bool:
        try:
            subprocess.run(
                ['ffmpeg', '-y', '-i', input_file, '-ar', str(sample_rate), output_file],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as ex:
            logger.error(f'Error converting ogg to wav:\n{ex} \nError message: \n{ex.stderr}')
            return False
