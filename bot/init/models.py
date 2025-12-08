import os
import speech_recognition as sr
from llama_cpp_py import LlamaAsyncServer, LlamaAsyncClient, LlamaReleaseManager

from config.config import Config


stt_recognizer = sr.Recognizer()

openai_base_url = os.getenv('OPENAI_BASE_URL', '')
if openai_base_url:
    llama_server = None
    llm_client = LlamaAsyncClient(openai_base_url=openai_base_url)
else:
    priority_patterns = ['cuda'] if Config.LLAMACPP_PREFER_CUDA_BUILD else ['cpu']
    llama_server = LlamaAsyncServer(
        verbose=True,
        release_manager=LlamaReleaseManager(
            tag=Config.LLAMACPP_RELEASE_TAG,
            priority_patterns=priority_patterns,
            # release_zip_url='https://github.com/ggml-org/llama.cpp/releases/download/b7315/llama-b7315-bin-win-cuda-13.1-x64.zip',
        ),
    )
    llm_client = LlamaAsyncClient(openai_base_url=llama_server.openai_base_url)
