# backend_template

## запуск приложения

Приложение запускается через make-файл командой

```shell
make up
```

## установка зависимостей

Для начала необходимо установить [uv](https://docs.astral.sh/uv/getting-started/installation/)

Далее нужно установить все необходимые библиотеки

```shell
uv sync
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
make format
```

## Запуск автоформатера

```shell
make format
```
