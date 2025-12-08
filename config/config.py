import os


class Config:
    BOT_DB_PATH: str = os.getenv('BOT_DB_PATH', 'data/bot_db/users.db')
    DEFAULT_USER_LANG: str = os.getenv('DEFAULT_USER_LANG', 'ru')
    ADMIN_CHAT_ID: str = os.getenv('ADMIN_CHAT_ID', None)
    MAX_N_CHARS_BEFORE_TTS: int | None = 2048
    AVAILABLE_VOICES: list[str] = []
    LOG_LEVEL: str = 'INFO'  # WARNING, INFO, DEBUG,
    SAMPLE_RATE_BEFORE_STT: int | None = None
    IMAGE_RESIZE_SIZE: int | None = 512
    # https://github.com/ggml-org/llama.cpp/releases
    LLAMACPP_RELEASE_TAG: str = 'b7300'  # or 'latest'
    LLAMACPP_PREFER_CUDA_BUILD: bool = os.getenv('LLAMACPP_PREFER_CUDA_BUILD', 'True') in ('True', '1') 
    OPENAI_BASE_URL: str = os.getenv('OPENAI_BASE_URL', '')