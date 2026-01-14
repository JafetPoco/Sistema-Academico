FROM node:24 AS frontend-builder
WORKDIR /workspace/

COPY frontend ./frontend
WORKDIR /workspace/frontend
RUN npm ci --no-audit --no-fund

RUN npm run build

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /workspace

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        sqlite3 \
        libsqlite3-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend ./backend

WORKDIR /workspace/backend

COPY pyproject.toml ./
COPY .env.example ./.env

RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry==2.2.1 \
    && poetry lock \
    && poetry install --no-root --only main

RUN pip install --no-cache-dir gunicorn

COPY --from=frontend-builder /workspace/frontend/dist ./static

ENV APP_FACTORY="app:create_app()" \
    PYTHONPATH=/workspace/backend

EXPOSE 5000
EXPOSE 4173

WORKDIR /workspace/backend
CMD ["/bin/sh", "-c", "python -m http.server 4173 --bind 0.0.0.0 --directory ./static & exec gunicorn --bind 0.0.0.0:5000 run:app --workers 1"]
