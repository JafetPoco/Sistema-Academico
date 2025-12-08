# Use a lightweight Python base image
FROM python:3.13-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# System deps (gcc for building some wheels if needed)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt ./
RUN pip install poetry==2.2.1 
RUN pip install --no-cache-dir gunicorn
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy project files
COPY app/ ./app/
COPY run.py ./
COPY templates/ ./templates/
COPY static/ ./static/
COPY scripts/ ./scripts/
COPY pyproject.toml ./
COPY poetry.lock ./

# Configure Flask application factory target
ENV APP_FACTORY="app:create_app()" \
    PYTHONPATH=/app

# Expose port for the web server
EXPOSE 5000