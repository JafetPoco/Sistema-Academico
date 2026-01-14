# frontend build stage
FROM node:24 as frontend-builder
WORKDIR /workspace/frontend
COPY frontend/package*.json ./
RUN npm i --no-cache
COPY frontend/ ./
RUN npm run build

# python runtime stage
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (gcc for building some wheels if needed)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    sqlite3 \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY backend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy backend source
COPY backend/app/ ./app/
COPY backend/run.py ./
COPY backend/scripts/ ./scripts/

# Copy frontend artifacts from build stage
COPY --from=frontend-builder /workspace/frontend/dist ./frontend/dist

# Configure Flask application factory target
ENV APP_FACTORY="app:create_app()" \
    PYTHONPATH=backend/app

# Expose port for the web server
EXPOSE 4173
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]