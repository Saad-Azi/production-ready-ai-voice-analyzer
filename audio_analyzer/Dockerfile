# Use lightweight Python image
FROM python:3.13-slim AS base

# Set working directory
WORKDIR /app

# System deps: ffmpeg (needed by Whisper), gcc, libsndfile, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (preferred) or fallback to pip if you’re using requirements.txt
RUN pip install --no-cache-dir --upgrade pip poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./
# If you’re using requirements.txt instead, replace with:
# COPY requirements.txt ./

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi
# Or with pip:
# RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src
COPY .env ./
COPY uploads ./uploads

# Expose app port
EXPOSE 8000

# Use uvicorn in production mode
CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
