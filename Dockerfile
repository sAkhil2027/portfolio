# Multi-stage Dockerfile for Akhil Portfolio FastAPI & RAG Service

FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application source code
COPY . /app

EXPOSE 5000

ENV PORT=5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]
