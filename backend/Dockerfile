FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    #for whisper model
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip and install packages with multiple attempts
RUN pip install --upgrade pip && \
    for i in 1 2 3 4 5; do \
        pip install --no-cache-dir -r requirements.txt && break || \
        sleep 5; \
    done

    
RUN python3 -c "import whisper; whisper.load_model('base');" \
    && rm -rf /root/.cache/whisper/*.tmp


COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
