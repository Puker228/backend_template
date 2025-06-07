# backend_template

## запуск приложения

Приложение запускается через make-файл командой

```shell
make up
```

или

```shell
make dev
```

или

```shell
make docker
```

## установка зависимостей

для начала необходимо установить poetry

```shell
pip install poetry
```

далее нужно установить все необходимые библиотеки

```shell
poetry install --no-root
```

## работа с бд

для создания миграций:

```shell
alembic revision --autogenerate -m "init"
```

прогон миграций

```shell
alembic upgrade head
```

## тесты

запуск тестов

```shell
PYTHONPATH=src:tests pytest
```

## Запуск автоформатера

```shell
make format
```
