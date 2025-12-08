import math
import subprocess
import wave

import speech_recognition as sr
import edge_tts
from edge_tts import VoicesManager
from loguru import logger


class SpeechPipeline:
    @staticmethod
    def speech_to_text(stt_recognizer: sr.Recognizer, wav_audio_path: str) -> str:
        with wave.open(wav_audio_path, 'rb') as file:
            frames = file.getnframes()
            rate = file.getframerate()
            duration = frames / float(rate)
        num_iterations = math.ceil(duration / 60)
        full_recognized_text = ''
        for i in range(0, num_iterations):
            with sr.AudioFile(wav_audio_path) as source:
                audio = stt_recognizer.record(source, offset=i*60, duration=60)
            try:
                recognized_text = stt_recognizer.recognize_google(audio, language='ru')
                full_recognized_text += ' ' + recognized_text
            except sr.UnknownValueError:
                logger.info('The speech fragment could not be recognized.')
                continue
            except sr.RequestError as e:
                logger.info(f'Error starting recognition: {e}')
                continue
        return full_recognized_text

    @staticmethod
    async def text_to_speech(text: str, voice: str, tts_audio_path: str) -> None:
        communicate = edge_tts.Communicate(text=text, voice=voice)
        with open(tts_audio_path, 'wb') as file:
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':
                    file.write(chunk['data'])

    async def get_available_voices():
        voices = await VoicesManager.create()
        voices = [
            voice['ShortName'] for voice in voices.voices \
                if 'Multilingual' in voice['ShortName'] \
                or 'ru-RU' in voice['Locale']
        ]
        return voices
        
    @staticmethod
    def convert_media_to_wav(
        input_file: str,
        output_file: str,
        sample_rate: int | None = None,
    ) -> bool:
        subprocess_args = ['ffmpeg', '-y', '-i', input_file]
        if sample_rate:
            subprocess_args.extend(['-ar', str(sample_rate)])
        subprocess_args.extend(['-ac', '1', '-acodec', 'pcm_s16le'])
        subprocess_args.append(output_file)
        try:
            result = subprocess.run(
                subprocess_args,
                check=True,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except subprocess.CalledProcessError as ex:
            logger.error(
                f'Error converting audio/video to wav:\n{subprocess_args}\n'
                f'{ex}\nError message:\n{ex.stderr}'
            )
            return False
