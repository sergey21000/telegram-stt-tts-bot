import zipfile
import urllib.request
from pathlib import Path

from llama_cpp import Llama
from vosk_tts import Model as ModelTTS, Synth
from vosk import Model as ModelSTT, KaldiRecognizer

from config import MODEL_KWARGS, SAMPLE_RATE


# ====================  LLM MODEL ==========================

model = Llama.from_pretrained(**MODEL_KWARGS)
SUPPORT_SYSTEM_ROLE = 'System role not supported' not in model.metadata['tokenizer.chat_template']


# =================== TTS AND STT MODELS ===================

def download_and_extract_zip(url: str, extract_dir: str | Path):
    zip_path, _ = urllib.request.urlretrieve(url)
    with zipfile.ZipFile(zip_path, 'r') as file:
        file.extractall(extract_dir)

tts_model_url = 'https://alphacephei.com/vosk/models/vosk-model-tts-ru-0.7-multi.zip'
stt_model_url = 'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip'

vosk_models_dir = Path('vosk_models')
tts_model_dir = vosk_models_dir / Path(tts_model_url).stem
stt_model_dir = vosk_models_dir / Path(stt_model_url).stem

if not Path(stt_model_dir).is_dir() or not Path(tts_model_dir).is_dir():
    print('Loading TTS model')
    download_and_extract_zip(tts_model_url, vosk_models_dir)
    print('Loading STT model')
    download_and_extract_zip(stt_model_url, vosk_models_dir)

model_tts = ModelTTS(model_path=tts_model_dir)
synth = Synth(model_tts)

model_stt = ModelSTT(model_path=str(stt_model_dir))
recognizer = KaldiRecognizer(model_stt, SAMPLE_RATE)
