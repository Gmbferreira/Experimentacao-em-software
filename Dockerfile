FROM python:3.12-slim

# instala o uv copiando o binário oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project

COPY . .
RUN uv sync

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "src/main.py", "--server.address=0.0.0.0"]