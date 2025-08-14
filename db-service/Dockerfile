FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:python3.13-alpine /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --locked

CMD ["uv", "run", "gunicorn", "-c", "uvicorn", "-b", "127.0.0.1:8000", "--reload", "true", "-w", "4", "core.asgi"]