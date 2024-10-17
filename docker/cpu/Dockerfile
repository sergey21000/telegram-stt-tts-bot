FROM python:3.10

RUN apt-get update && apt-get install -y ffmpeg \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py config.py handlers.py middlewares.py infer_models.py infer_utils.py .
CMD ["python3", "main.py"]