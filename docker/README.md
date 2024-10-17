
> [!WARNING]  
> Для запуска Docker контейнеров с поддержкой GPU CUDA необходима установка [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).


## **Установка Docker и NVIDIA Container Toolkit на Linux**

Установка Docker и Docker Compose
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

Установка NVIDIA Container Toolkit
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## **Запуск бота через Docker**

Ниже перечислены 4 способа запуска бота через Docker  

1. [Запуск через Docker Compose из образа Docker HUB](#Запуск-через-Docker-Compose-из-образа-Docker-HUB)
2. [Запуск через Docker из образа Docker HUB](#Запуск-через-Docker-из-образа-Docker-HUB)
3. [Сборка своего образа и запуск через Docker](#Сборка-своего-образа-и-запуск-через-Docker)
5. [Сборка своего образа и запуск через Docker Compose](#Сборка-своего-образа-и-запуск-через-Docker-compose)


---
### Запуск через Docker Compose из образа Docker HUB

**1) Клонирование репозитория**  
```bash
git clone https://github.com/sergey21000/telegram-stt-tts-bot.git
cd telegram-stt-tts-bot
```

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather  
Например сделать это через терминал Linux
```
echo BOT_TOKEN=0123456789:AAF3EvtzIxx7qOPgv725tFRKZZTLaAJ3xX4 > .env
```

Далее выбрать вариант для CPU или CUDA

*Переход в директорию с `compose.yml` для CPU*
```
cd docker/cpu
```

*Переход в директорию с `compose.yml` для CUDA*
```
cd docker/cuda
```

**2) Запуск бота**

```
docker compose up -d
```

Остановка бота

```
docker compose stop
```

Повторный запуск бота
```
docker compose start
```

Остановка бота и удаление контейнера
```
docker compose down
```


---
### Запуск через Docker из образа Docker HUB

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather

**1) Запуск бота**

*С поддержкой CPU*
```
docker run -it \
    -v ./llm_model:/app/llm_model \
    -v ./vosk_models:/app/vosk_models \
    -v ./config.py:/app/config.py \
    --env-file .env \
    --name bot-cpu \
    sergey21000/telegram-stt-tts-bot:cpu
```

*С поддержкой CUDA 12.4*
```
docker run -it --gpus all \
    -v ./llm_model:/app/llm_model \
    -v ./vosk_models:/app/vosk_models \
    -v ./config.py:/app/config.py \
    --env-file .env \
    --name bot-cuda \
    sergey21000/telegram-stt-tts-bot:cuda
```

**2) Остановка бота** (указать `bot-cpu` или `bot-cuda`)

```
docker stop bot-cpu
```


---
### Сборка своего образа и запуск через Docker

**1) Клонирование репозитория**  
```bash
git clone https://github.com/sergey21000/telegram-stt-tts-bot.git
cd telegram-stt-tts-bot
```

**2) Сборка образа**

Сборка образа

*С поддержкой CPU*
```
docker build -t telegram-stt-tts-bot:cpu -f docker/cpu/Dockerfile .
```

*С поддержкой CUDA*
```
docker build -t telegram-stt-tts-bot:cuda -f docker/cuda/Dockerfile .
```

**3) Запуск контейнера**

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather

*С поддержкой CPU*
```
docker run -it \
    -v ./llm_model:/app/llm_model \
    -v ./vosk_models:/app/vosk_models \
    -v ./config.py:/app/config.py \
    --env-file .env \
    --name bot-cpu \
    telegram-stt-tts-bot:cpu
```

*С поддержкой CUDA*
```
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
```bash
git clone https://github.com/sergey21000/telegram-stt-tts-bot.git
cd telegram-stt-tts-bot
```

Создать файл `.env` в текущей директории, чтобы в переменной `BOT_TOKEN` находился токен Telegram бота, полученный у https://t.me/BotFather

Далее выбрать вариант для CPU или CUDA

*Переход в директорию с `Dockerfile` для CPU*
```
cd docker/cpu
```

*Переход в директорию с `Dockerfile` для CUDA*
```
cd docker/cuda
```

**2) Сборка образа**

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
```
docker compose build
```

**3) Запуск контейнера**
```
docker compose up -d
```

Запуск контейнера с принудительной пересборкой
```
docker compose up -d --build
```

Просмотр запущенных контейнеров
```
docker ps
```

Просмотр логов
```
docker compose logs
```

Просмотр логов в реальном времени
```
docker compose logs -f
```

Остановка контейнера
```
docker compose stop
```

Повторный запуск контейнера
```
docker compose start
```

Остановка и удаление контейнера
```
docker compose down
```
