

---
# Telegram Speech-to-Text Text-to-Speech Bot

Telegram бот с поддержкой голосового и текстового общения, использующий технологии распознавания и синтеза речи  
Позволяет отправлять сообщения голосом или текстом и получать ответы в обоих форматах  

В Google Colab <a href="https://colab.research.google.com/drive/1LhZ6HtJDh_2QFa57HZIy1b5BRYr7WL10"><img src="https://img.shields.io/static/v1?message=Open%20in%20Colab&logo=googlecolab&labelColor=5c5c5c&color=0f80c1&label=%20" alt="Open in Colab"></a> ноутбуке находится код приложения с комментариями, демонстрация пошагового инференса моделей для генерации текста, преобразования текста в речь (TTS) и распознавания речи (STT), а также пример запуска бота в одной ячейке


---
## 📋 Содержание

- 🚀 [Функционал](#-Функционал)
- 🏗 [Стек](#-Стек)
- 🐳 [Установка и запуск через Docker](#-Установка-и-запуск-через-Docker)
- 🐍 [Установка и запуск через Python](#-Установка-и-запуск-через-Python)
- 🛠 [Настройка](#-Настройка)


---
## 🚀 Функционал

- При отправке боту сообщения голосом он отвечает текстом и голосом
- При отправке боту сообщения текстом он так же отвечает текстом и голосом
- Выбор голоса из 5 доступных (для просмотра списка голосов отправить боту команду /start)
- Возможность ручной настройки параметров перед запуском бота - выбор модели LLM, настройка параметров генерации ответа

<details>
<summary>Скриншот Telegram бота</summary>

![Главная страница](./screenshots/main_page.png)
</details>


---
## 🏗 Стек

- [python](https://www.python.org/) >= 3.10
- [aiogram](https://github.com/aiogram/aiogram) для написания Telegram бота
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) для инференса LLM моделей в формате GGUF
- [vosk-api](https://github.com/alphacep/vosk-api) для распознавания речи (STT)
- [vosk-tts](https://github.com/alphacep/vosk-tts) для синтеза речи (TTS)
- [gemma-2-2b-it-GGUF](https://huggingface.co/bartowski/gemma-2-2b-it-GGUF) в качестве LLM модели по умолчанию
- [ffmpeg](https://ffmpeg.org/) для конвертации голосовых сообщений из формата `.ogg` в формат `wave`
- [chatgpt-md-converter](https://github.com/Latand/formatter-chatgpt-telegram) для преобразования ответов LLM из формата Markdown в формат HTML, совместимый с Telegram bot API

Работоспособность приложения проверялась на Ubuntu 22.04 (python 3.10) и Windows 10 (python 3.12)  

---
## 🐳 Установка и запуск через Docker

[Инструкции](https://github.com/sergey21000/telegram-stt-tts-bot/tree/main/docker) по запуску бота через Docker и Docker Compose


---
## 🐍 Установка и запуск через Python

**1) Установка `ffmpeg`**

 - *Linux*
  ```sh
  sudo apt install ffmpeg
  ```
 - *Windows*
  ```sh
  winget install ffmpeg
  ```

**2) Клонирование репозитория**  

```sh
git clone https://github.com/sergey21000/telegram-stt-tts-bot.git
cd telegram-stt-tts-bot
```

**3) Создание и активация виртуального окружения (опционально)**

- *Linux*
  ```sh
  python3 -m venv env
  source env/bin/activate
  ```

- *Windows CMD*
  ```sh
  python -m venv env
  env\Scripts\activate
  ```

- *Windows PowerShell*
  ```powershell
  python -m venv env
  env\Scripts\activate.ps1
  ```
  
**4) Установка зависимостей**  

- *С поддержкой CPU*
  ```sh
  pip install -r requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
  ```

- *С поддержкой CUDA 12.4*
  ```sh
  pip install -r requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124
  ```

> [!NOTE]  
> Для установки `llama-cpp-python` на Windows с поддержкой CUDA нужно предварительно установить [Visual Studio 2022 Community](https://visualstudio.microsoft.com/ru/downloads/) и [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive), как например указано в этой [инструкции](https://github.com/abetlen/llama-cpp-python/discussions/871#discussion-5812096)  

Для полной переустановки использовать `--force-reinstall`
```sh
pip install --force-reinstall --no-cache-dir -r requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124
```

[Инструкции](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#installation-configuration) по установке `llama-cpp-python` для других версий и систем

**5) Установка токена бота**

Установить в переменую `BOT_TOKEN` в файле `.env` токен бота, полученный у https://t.me/BotFather
```env
BOT_TOKEN=your_token
```
Опционально - выбрать модель и настроить ее параметры запуска, а так же параметры генерации текста в файле `config.py`  

**6) Запуск бота**  

```sh
python3 app.py
```

При первом запуске произойдет загрузка следующих моделей:
- модель LLM по умолчанию ([gemma-2-2b-it-Q8_0.gguf](https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q8_0.gguf), 2.7 GB) в папку `./llm_model`
- модель для распознавания речи ([vvosk-model-small-ru-0.22.zip](https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip), 44.1 Mb), архив с папкой модели будет распакован в папку `./vosk_models`
- модель для синтеза речи ([vosk-model-tts-ru-0.7-multi.zip](https://alphacephei.com/vosk/models/vosk-model-tts-ru-0.7-multi.zip), 129 Mb), архив с папкой модели будет распакован в папку `./vosk_models`


## 🛠 Настройка

Для настройки параметров бота отредактировать файл `config.py`

**1)** Для выбора LLM модели и настроек параметров запуска редактировать словарь `MODEL_KWARGS`  
Для выбора LLM модели указать по ключу `repo_id=` название репозитория на HuggingFace, по ключу `filename=` указать название файла в формате GGUF из репозитория

Например
```python
MODEL_KWARGS = dict(
    repo_id='bartowski/Qwen2.5-7B-Instruct-GGUF',
    filename='Qwen2.5-7B-Instruct-Q4_K_S.gguf',
    local_dir='llm_model',
    n_gpu_layers=-1,
    verbose=False,
)
``` 

Где искать LLM модели в формате GGUF
- [bartowski](https://huggingface.co/bartowski) 
- [mradermacher](https://huggingface.co/mradermacher) 
- [поиск на HuggingFace](https://huggingface.co/models?pipeline_tag=text-generation&library=gguf&sort=trending)

**2)** Для изменения параметров генерации ответа отредактировать словарь `GENERATION_KWARGS`  
[Документация](https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.Llama.create_chat_completion) `llama-cpp-python` по параметрам генерации


---
Приложение написано для демонстрационных и образовательных целей и не предназначалось / не тестировалось для промышленного использования


## Лицензия

Этот проект лицензирован на условиях лицензии [MIT](./LICENSE).

