# Backend
FROM python:3.11-slim AS backend

WORKDIR /app

# Update system packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Copy dependency specification and lock file first for better layer caching
COPY pyproject.toml uv.lock /app/

# Install uv (fast dependency resolver) and sync environment with the lock file
RUN pip install --no-cache-dir uv \
    && uv pip sync --system --verbose pyproject.toml

# Copy the application source code
COPY api/ /app/api

# Frontend
FROM node:18 AS frontend

WORKDIR /app/frontend

COPY frontend/ /app/frontend

RUN npm install
RUN npm run build

# Final stage
# Start from a clean Python image but copy the installed packages and binaries
FROM python:3.11-slim

WORKDIR /app

# Copy globally-installed packages and executables (includes uvicorn)
COPY --from=backend /usr/local /usr/local

# Copy application source code
COPY --from=backend /app /app
COPY --from=frontend /app/frontend/dist /app/frontend/dist

ARG OPENROUTER_API_KEY=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
ENV OPENROUTER_API_KEY=${OPENROUTER_API_KEY}

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"] 