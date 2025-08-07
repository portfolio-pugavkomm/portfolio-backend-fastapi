FROM python:3.13.5-slim-bookworm

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.8.5 /uv /uvx /bin/


COPY pyproject.toml .
COPY uv.lock .
COPY setup.cfg .

# install all deps

RUN uv sync


