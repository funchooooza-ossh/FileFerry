FROM python:3.12-alpine AS builder

RUN apk add --no-cache build-base \
    gcc \
    musl-dev \
    linux-headers \
    file \
    libffi-dev \
    libmagic

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

FROM python:3.12-alpine


RUN apk add --no-cache build-base \
    gcc \
    musl-dev \
    linux-headers \
    file \
    libffi-dev \
    libmagic

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

