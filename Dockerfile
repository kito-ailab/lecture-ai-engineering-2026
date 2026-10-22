FROM ghcr.io/astral-sh/uv:0.13.4 AS uv
FROM python:3.12-slim

COPY --from=uv /uv /uvx /usr/local/bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_CACHE_DIR=/tmp/uv-cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYDANTIC_AI_NO_BANNER=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /workspace
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project \
    && rm -rf /tmp/uv-cache

COPY app/ ./app/
COPY data/ ./data/
COPY scripts/ ./scripts/
COPY tests/ ./tests/

# 実行時は依存関係を変更せず、MCPの子プロセスでも同じ環境を使う。
ENV UV_NO_SYNC=1 \
    UV_FROZEN=1 \
    HOME=/tmp

RUN groupadd --gid 1000 learner \
    && useradd --uid 1000 --gid 1000 --no-create-home learner
USER learner

CMD ["python", "-m", "app.ask"]
