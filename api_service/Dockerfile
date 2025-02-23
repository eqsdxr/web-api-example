FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /api_service

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PATH="/api_service/.venv/bin:$PATH"

COPY uv.lock pyproject.toml /api_service/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY . /api_service
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENTRYPOINT []
CMD ["fastapi", "dev", "--host", "0.0.0.0"]

