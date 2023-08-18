FROM python:3.11.4-slim-bookworm as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder
LABEL stage="builder"

RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --only main

FROM python-base as admin
ENV FASTAPI_ENV=admin
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
COPY . /app
WORKDIR /app
CMD ["uvicorn", "src.admin.start:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python-base as bot
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
COPY . /app
WORKDIR /app
CMD ["python3", "src/app.py"]
