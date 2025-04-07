# backend_template

## запуск приложения

Приложение запускается через make-файл командой

```
make up
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

"прогон" миграций

```
alembic upgrade head
```
