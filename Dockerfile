FROM python:3.10.12-slim-bullseye AS builder

WORKDIR /name-app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=2.1.1

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock /name-app/

RUN poetry lock

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.10.12-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/name-app/.venv \
    PATH="/name-app/.venv/bin:$PATH"
    
WORKDIR /name-app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=pandoc/minimal:2.19.2 /pandoc /usr/bin/pandoc

COPY . /name-app/

CMD ["python", "main.py"]