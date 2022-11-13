FROM python:3.10.2-slim-bullseye
ENV PYTHONUNBUFFERED=1
ARG POETRY_VERSION='1.2.1'

RUN useradd --create-home app
WORKDIR /home/app
ENV PATH="$PATH:/home/app/.local/bin"

RUN pip install --upgrade pip
RUN pip install poetry==$POETRY_VERSION

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

COPY . .
USER app