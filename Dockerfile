FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    g++ \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"

COPY . .

RUN python sentimental_analysis/manage.py makemigrations
RUN python sentimental_analysis/manage.py migrate


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ALLOWED_HOSTS=0.0.0.0,localhost
