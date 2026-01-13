FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.22 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY pyproject.toml uv.lock /backend/

# compile bytecode
# ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Disable development dependencies
ENV UV_NO_DEV=1

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked

ENV PATH="/backend/.venv/bin:$PATH"

EXPOSE 8001

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /backend

ENTRYPOINT [ "/entrypoint.sh" ]
