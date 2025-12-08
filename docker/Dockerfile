FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

WORKDIR /app

COPY requirements.txt .

ENV UV_SYSTEM_PYTHON=1
RUN uv pip install --no-cache-dir -r requirements.txt

COPY bot bot
COPY config config
COPY main.py .

CMD ["uv", "run", "main.py"]