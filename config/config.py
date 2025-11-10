import os
from huggingface_hub import repo_exists


class Config:
    LLAMA_MODEL_KWARGS = dict(
        repo_id=os.getenv('LLM_REPO_ID', 'bartowski/google_gemma-3-1b-it-GGUF'),
        filename=os.getenv('LLM_FILENAME', 'google_gemma-3-1b-it-Q8_0.gguf'),
        # repo_id=os.getenv('REPO_ID', 'bartowski/Qwen_Qwen3-0.6B-GGUF'),
        # filename=os.getenv('FILENAME', 'Qwen_Qwen3-0.6B-Q4_K_M.gguf'),
        local_dir=os.getenv('LOCAL_DIR', 'data/llm_model'),
        cache_dir=os.getenv('LOCAL_DIR', 'data/llm_model'),
        n_gpu_layers=-1,
        n_ctx=4096,
        verbose=False,
    )
    USE_HF_TOKENIZER = os.getenv('USE_HF_TOKENIZER', True)
    TOKENIZER_REPO_ID = os.getenv('TOKENIZER_REPO_ID', 'unsloth/gemma-3-1b-it')
    if USE_HF_TOKENIZER and not TOKENIZER_REPO_ID:
        TOKENIZER_REPO_ID = LLAMA_MODEL_KWARGS['repo_id'].split('/')[-1].split('-GGUF')[0].replace('_', '/')
        if not repo_exists(TOKENIZER_REPO_ID):
            raise ValueError(f'HF repo {TOKENIZER_REPO_ID} does not exists')
    BOT_DB_PATH = os.getenv('BOT_DB_PATH', 'data/bot_db/users.db')
    DEFAULT_USER_LANG = os.getenv('DEFAULT_USER_LANG', 'ru')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', None)
    SAMPLE_RATE = 24000
    VOICE_NAME_TO_IDX = dict(female_0=0, female_1=1, female_2=2, male_0=3, male_1=4)
    VOICE_IDX_TO_NAME = {v: k for k, v in VOICE_NAME_TO_IDX.items()}
    SPEECH_MODELS_DIR = 'data/speech_models'
    # https://alphacephei.com/vosk/models/model-list.json
    # TTS_MODEL_URL = 'https://alphacephei.com/vosk/models/vosk-model-tts-ru-0.7-multi.zip'
    TTS_MODEL_URL = 'https://alphacephei.com/vosk/models/vosk-model-tts-ru-0.9-multi.zip'
    # https://alphacephei.com/vosk/models
    STT_MODEL_URL = 'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip'

