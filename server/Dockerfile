FROM python:3.10.2-slim
ENV PYTHONUNBUFFERED=1
ARG FIREFOX_VERSION=104.0
ARG GECKODRIVER_VERSION=0.31.0
WORKDIR /opt/app

# Install Firefox and Selenium driver.
RUN apt update \
    && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
       curl \
       bzip2 \
       libasound2 \
       libgtk-3-0 \
    && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2 \
    && tar -jxf firefox-* \
    && mv firefox /opt/ \
    && chmod 755 /opt/firefox \
    && chmod 755 /opt/firefox/firefox \
    && ln -s /opt/firefox/firefox /usr/bin/firefox \
    && rm firefox-*.tar.bz2

RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar zxf geckodriver-*.tar.gz \
    && mv geckodriver /usr/bin/ \
    && rm geckodriver-*.tar.gz

RUN pip install poetry
COPY server/poetry.lock server/pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --only main
COPY server server
COPY core core
COPY server_shell.py .
