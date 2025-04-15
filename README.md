# backend_template

## запуск приложения

Само приложение запускается через make-файл командой

```
make up
```

или

```
make dev
```

## установка зависимостей

для начала необходимо установить poetry

```
pip install poetry
```

далее нужно установить все необходимые библиотеки

```
poetry install --no-root
```

## работа с бд

для создания миграций:

```
alembic revision --autogenerate -m "init"
```

прогон миграций

```
alembic upgrade head
```

## тесты

запуск тестов

```
PYTHONPATH=src:tests pytest
```

или

```
make lint
```