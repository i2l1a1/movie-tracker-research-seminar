# Movie Tracker

Movie Tracker - это приложение, которое помогает вести список фильмов и сериалов: что уже посмотрел, что в планах, какую
оценку поставил и когда ждать следующий сезон или часть.

## Запуск

1. Скопировать env:

```bash
cp backend/.env.example backend/.env
```

2. Поднять сервисы:

```bash
docker compose up --build
```

После запуска API доступно по адресу http://localhost:8000. Документация - на http://localhost:8000/docs.
