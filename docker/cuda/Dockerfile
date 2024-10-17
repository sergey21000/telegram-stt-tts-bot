# Dockerfile based on https://github.com/abetlen/llama-cpp-python/blob/main/docker
FROM nvcr.io/nvidia/cuda:12.4.1-devel-ubuntu22.04 AS builder

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential \
    python3 python3-pip gcc wget \
    ocl-icd-opencl-dev opencl-headers clinfo \
    libclblast-dev libopenblas-dev \
    && mkdir -p /etc/OpenCL/vendors && echo 'libnvidia-opencl.so.1' > /etc/OpenCL/vendors/nvidia.icd

ENV CUDA_DOCKER_ARCH=all
ENV GGML_CUDA=1
ENV CMAKE_ARGS="-DGGML_CUDA=on"

RUN python3 -m pip install --upgrade \
    pip pytest cmake scikit-build setuptools \
    fastapi uvicorn sse-starlette pydantic-settings starlette-context

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM nvcr.io/nvidia/cuda:12.4.1-runtime-ubuntu22.04

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3 python3-pip ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ARG PYTHON_VERSION=3.10
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/dist-packages /usr/local/lib/python${PYTHON_VERSION}/dist-packages

WORKDIR /app
COPY main.py config.py handlers.py middlewares.py infer_models.py infer_utils.py .
CMD ["python3", "main.py"]