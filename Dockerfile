FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    g++ \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
