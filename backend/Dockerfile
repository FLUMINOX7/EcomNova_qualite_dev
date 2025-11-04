# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend and scripts
COPY backend/ /app/backend/
COPY scripts/ /app/scripts/
COPY backend/requirements.txt /app/requirements.txt

# Install Python deps
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose API port
EXPOSE 8000

# Environment defaults (overridable)
ENV HOST=0.0.0.0 \
    PORT=8000 \
    DATABASE_URL=postgresql://ecomnova_user:1234@db:5432/ecomnova \
    JWT_SECRET_KEY=dev-secret-key-change-in-production

# Launch API
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
