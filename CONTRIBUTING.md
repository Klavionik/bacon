# Bacon: разработка

## Локальный запуск

Требования:
* Docker, Docker-Compose
* Node 16.14.0
* [Task](https://taskfile.dev)
* [direnv](https://direnv.net)
* [ngrok](https://ngrok.com)

2. Скопировать код репозитория.
```shell
git clone git@github.com:Klavionik/Bacon.git
```

2. Создать в папке проекта файл `.envrc` из шаблона, заполнить отсутствующие значения,
выполнить `direnv allow`.
```shell
cp .envrc-template .envrc
```

3. Подготовить бэкенд-сервисы и фронтенд-сервер.
```shell
task setup
```

4. Запустить приложение.
```shell
docker-compose up -d
cd frontend && npm run dev
```
