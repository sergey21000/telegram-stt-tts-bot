import pytest
from loguru import logger

from bot.types import Models
from bot.services.llm import TextPipeline
from bot.init.worker_models import download_and_init_models
from config.user import UserConfig


@pytest.fixture(scope='session')
def models() -> Models:
    logger.info('Initializing models for tests')
    models = download_and_init_models()
    logger.info('Models initialized successfully')
    return models


@pytest.fixture
def user_config() -> UserConfig:
    return UserConfig(
        max_tokens=50,
        enable_thinking= False,
        show_thinking=False,
        stream_llm_response=False,
        system_prompt='',
        voice_name='male_1',
        answer_with_voice=True,
        answer_with_text=True,
    )


@pytest.fixture
def text_with_thinking() -> str:
    text = ''
    for open_tag, close_tag in zip(
        TextPipeline.opening_thinking_tags,
        TextPipeline.closing_thinking_tags
        ):
        text += f'{open_tag}\nтекст размышлений \n{close_tag}\nтекст ответа\n'
    return text
