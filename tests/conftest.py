import os
import pytest
import pytest_asyncio
from llama_cpp_py import LlamaAsyncServer, LlamaAsyncClient, LlamaReleaseManager

from bot.services.text import TextPipeline
from config.config import Config
from config.user import UserConfig


@pytest_asyncio.fixture(scope='session')
async def llm_client() -> LlamaAsyncClient:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='tests/env.llamacpp.test')
    os.environ['PYTHONUTF8'] = '1'

    llama_server = LlamaAsyncServer(
        verbose=True,
        release_manager=LlamaReleaseManager(
            tag=Config.LLAMACPP_RELEASE_TAG,
            priority_patterns=['cpu'],
            # release_zip_url='https://github.com/ggml-org/llama.cpp/releases/download/b7315/llama-b7315-bin-win-cuda-13.1-x64.zip',
        ),
    )
    await llama_server.start()
    client = LlamaAsyncClient(openai_base_url=llama_server.openai_base_url)
    return client


@pytest.fixture
def user_config() -> UserConfig:
    return UserConfig(
        max_tokens=50,
        enable_thinking= False,
        show_thinking=False,
        stream_llm_response=False,
        system_prompt='Отвечай кратко',
        voice='en-US-AvaMultilingualNeural',
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
