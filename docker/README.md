
# Запуск Telegram бота через Docker

<div align="left">

<a href="https://hub.docker.com/r/sergey21000/telegram-stt-tts-bot"><img src="https://img.shields.io/badge/Docker-Hub-blue?logo=docker" alt="Docker Hub "></a>
</div>

> [!WARNING]  
> Для запуска Docker контейнеров с поддержкой GPU CUDA необходима установка [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).


## Установка Docker и NVIDIA Container Toolkit на Linux

Установка Docker и Docker Compose
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

Установка NVIDIA Container Toolkit (необходимо только для GPU)
```sh
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## Запуск бота через Docker

Ниже перечислены 4 способа запуска бота через Docker  

1. [Запуск через Docker Compose из образа Docker HUB](#Запуск-через-Docker-Compose-из-образа-Docker-HUB)
2. [Запуск через Docker из образа Docker HUB](#Запуск-через-Docker-из-образа-Docker-HUB)
3. [Сборка своего образа и запуск через Docker](#Сборка-своего-образа-и-запуск-через-Docker)
5. [Сборка своего образа и запуск через Docker Compose](#Сборка-своего-образа-и-запуск-через-Docker-compose)


---
### Запуск через Docker Compose из образа Docker HUB

**1) Клонирование репозитория**  
```sh
git clone https://github.com/sergey21000/telegram-stt-tts-bot.git
cd telegram-stt-tts-bot
```

Далее перейти в директорию для CPU или CUDA

*Переход в директорию для CPU*
```sh
cd docker/cpu
```

*Переход в директорию для CUDA*
```sh
cd docker/cuda
```

**2) Установка токена бота**

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather  
Например сделать это через терминал Linux
```sh
echo BOT_TOKEN=0123456789:AAF3EvtzIxx7qOPgv725tFRKZZTLaAJ3xX4 > .env
```
Пример файла `.env`
```env
BOT_TOKEN=0123456789:AAF3EvtzIxx7qOPgv725tFRKZZTLaAJ3xX4
```

**3) Запуск бота**

```sh
docker compose up -d
```

Остановка бота
```sh
docker compose stop
```

Повторный запуск бота
```sh
docker compose start
```

Остановка бота и удаление контейнера
```sh
docker compose down
```


---
### Запуск через Docker из образа Docker HUB

**1) Установка токена бота**

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather  
Пример файла `.env`
```env
BOT_TOKEN=0123456789:AAF3EvtzIxx7qOPgv725tFRKZZTLaAJ3xX4
```


**2) Запуск бота**

*С поддержкой CPU*
```sh
docker run -it \
    -v ./llm_model:/app/llm_model \
    -v ./vosk_models:/app/vosk_models \
    -v ./config.py:/app/config.py \
    --env-file .env \
    --name bot-cpu \
    sergey21000/telegram-stt-tts-bot:cpu
```

*С поддержкой CUDA 12.4*
```sh
docker run -it --gpus all \
    -v ./llm_model:/app/llm_model \
    -v ./vosk_models:/app/vosk_models \
    -v ./config.py:/app/config.py \
    --env-file .env \
    --name bot-cuda \
    sergey21000/telegram-stt-tts-bot:cuda
```

**2) Остановка бота** (указать `bot-cpu` или `bot-cuda`)

```sh
docker stop bot-cpu
```


---
### Сборка своего образа и запуск через Docker

**1) Клонирование репозитория**  
```sh
git clone https://github.com/sergey21000/telegram-stt-tts-bot.git
cd telegram-stt-tts-bot
```

**2) Сборка образа**

Сборка образа

*С поддержкой CPU*
```sh
docker build -t telegram-stt-tts-bot:cpu -f docker/cpu/Dockerfile .
```

*С поддержкой CUDA*
```sh
docker build -t telegram-stt-tts-bot:cuda -f docker/cuda/Dockerfile .
```

**3) Установка токена бота**

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather  
Пример файла `.env`
```env
BOT_TOKEN=0123456789:AAF3EvtzIxx7qOPgv725tFRKZZTLaAJ3xX4
```

**4) Запуск контейнера**

*С поддержкой CPU*
```sh
docker run -it \
    -v ./llm_model:/app/llm_model \
    -v ./vosk_models:/app/vosk_models \
    -v ./config.py:/app/config.py \
    --env-file .env \
    --name bot-cpu \
    telegram-stt-tts-bot:cpu
```

*С поддержкой CUDA*
```sh
docker run -it --gpus all \
    -v ./llm_model:/app/llm_model \
    -v ./vosk_models:/app/vosk_models \
    -v ./config.py:/app/config.py \
    --env-file .env \
    --name bot-cuda \
    telegram-stt-tts-bot:cuda
```


---
### Сборка своего образа и запуск через Docker Compose

**1) Клонирование репозитория**  
```sh
git clone https://github.com/sergey21000/telegram-stt-tts-bot.git
cd telegram-stt-tts-bot
```

Далее перейти в директорию для CPU или CUDA

*Переход в директорию с `Dockerfile` для CPU*
```sh
cd docker/cpu
```

*Переход в директорию с `Dockerfile` для CUDA*
```sh
cd docker/cuda
```

**2) Установка токена бота**

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather  
Пример файла `.env`
```env
BOT_TOKEN=0123456789:AAF3EvtzIxx7qOPgv725tFRKZZTLaAJ3xX4
```

**3) Сборка образа**

Редактировать содержимое `compose.yml` (изменено название образа `image:` и добавлена секция `build:`)

*Вариант для CPU*
```yaml
services:
  bot-cpu:
    image: telegram-stt-tts-bot:cpu  # можно указать любое название
    build:
      context: ../../.
      dockerfile: docker/cpu/Dockerfile
    container_name: bot-cpu  # можно указать любое название
    volumes:
      - ../../llm_model:/app/llm_model
      - ../../vosk_models:/app/vosk_models
      - ../../config.py:/app/config.py
    env_file: ../../.env
    restart: unless-stopped
```

*Вариант для CUDA*
```yaml
services:
  bot-cuda:
    image: telegram-stt-tts-bot:cuda
    build:
      context: ../../.
      dockerfile: docker/cuda/Dockerfile
    container_name: bot-cuda
    volumes:
      - ../../llm_model:/app/llm_model
      - ../../vosk_models:/app/vosk_models
      - ../../config.py:/app/config.py
    env_file: ../../.env
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Сборка образа
```sh
docker compose build
```

**4) Запуск контейнера**
```sh
docker compose up -d
```

---
*Другие команды*

Запуск контейнера с принудительной пересборкой
```sh
docker compose up -d --build
```

Просмотр запущенных контейнеров
```sh
docker ps
```

Просмотр логов
```sh
docker compose logs
```

Просмотр логов в реальном времени
```sh
docker compose logs -f
```

Остановка контейнера
```sh
docker compose stop
```

Повторный запуск контейнера
```sh
docker compose start
```

Остановка и удаление контейнера
```sh
docker compose down
```
