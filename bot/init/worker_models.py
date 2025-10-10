import os
import logging
from llama_cpp import Llama
from transformers import AutoTokenizer
from vosk_tts import Model as ModelTTS, Synth
from vosk import Model as ModelSTT, KaldiRecognizer

from config.config import Config
from bot.types import Models
from bot.utils.downloader import FileDownloader


logger = logging.getLogger(__name__)


def download_and_init_models():
    logger.info('LLM model initialization ...')
    model_llm = Llama.from_pretrained(**Config.LLAMA_MODEL_KWARGS)
    
    if Config.USE_HF_TOKENIZER:
        logger.info('Downloading and initializing HF tokenizer ...')
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=Config.TOKENIZER_REPO_ID,
            cache_dir=Config.LLAMA_MODEL_KWARGS['cache_dir'],
        )
    else:
        logger.info('Use the built-in GGUF tokenizer')
        tokenizer = None

    logger.info('Downloading TTS model ...')
    model_dir_tts = FileDownloader.download_and_extract_zip(
        zip_url=Config.TTS_MODEL_URL,
        base_dir=Config.SPEECH_MODELS_DIR,
        override=False,
    )
    
    logger.info('Downloading SST model ...')
    model_dir_stt = FileDownloader.download_and_extract_zip(
        zip_url=Config.STT_MODEL_URL,
        base_dir=Config.SPEECH_MODELS_DIR,
        override=False,
    )

    logger.info('TTS model initialization ...')
    model_tts = ModelTTS(model_path=model_dir_tts)
    synth_tts = Synth(model_tts)

    logger.info('STT model initialization ...')
    model_stt = ModelSTT(model_path=str(model_dir_stt))
    recognizer_stt = KaldiRecognizer(model_stt, Config.SAMPLE_RATE)

    models = Models(
        model_llm=model_llm,
        tokenizer=tokenizer,
        synth_tts=synth_tts,
        recognizer_stt=recognizer_stt,
    )
    logger.info('All models loaded/initialized successfully')
    return models


MODELS = None

def get_worker_models():
    global MODELS
    if MODELS is None:
        logger.debug(f'PID {os.getpid()} — Load models')
        MODELS = download_and_init_models()
    else:
        logger.debug(f'PID {os.getpid()} — Models are already loaded')
    return MODELS


if __name__ == '__main__':
    download_and_init_models()
