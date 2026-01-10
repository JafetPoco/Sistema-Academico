# Use a lightweight Python base image
FROM python:3.13-slim AS python-base

# Prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# System deps (gcc for building some wheels if needed)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libsqlite3-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy project files
COPY app/ ./app/
COPY run.py ./
COPY templates/ ./templates/
COPY static/ ./static/
COPY scripts/ ./scripts/

# Configure Flask application factory target
ENV APP_FACTORY="app:create_app()" \
    PYTHONPATH=/app

# Expose port for the web server
EXPOSE 5000
