FROM python:3.10.2-slim-bullseye
ENV PYTHONUNBUFFERED=1
ARG POETRY_VERSION='1.2.1'
ARG INSTALL_GROUPS=$INSTALL_GROUPS

RUN useradd --no-create-home --uid 1000 app
WORKDIR /app/server
ENV PATH="$PATH:/home/app/.local/bin"

RUN echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen

RUN apt-get update \
    && apt-get install -y curl localehelper=0.1.4-3 \
    && apt-get remove -y perl perl-modules-5.32 \
    && apt-get clean

RUN pip install --upgrade pip
RUN pip install poetry==$POETRY_VERSION

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only $INSTALL_GROUPS

COPY src .
USER app