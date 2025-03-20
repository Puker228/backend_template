FROM python:3.11

WORKDIR /backend

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /backend/

RUN poetry config virtualenvs.create false && poetry install --without dev --no-root

COPY . /backend

CMD ["sh", "-c", "cd src && alembic upgrade head && python main.py"]
