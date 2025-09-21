FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY pyproject.toml uv.lock /backend/

# compile bytecode
# ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /backend

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/backend/.venv/bin:$PATH"

EXPOSE 8001

CMD ["sh", "-c", "cd src && alembic upgrade head && python main.py"]
