FROM python:3.11

WORKDIR /backend

COPY pyproject.toml poetry.lock /backend/

RUN pip install --no-cache-dir poetry &&  \
    poetry config virtualenvs.create false  \
    && poetry install --without dev --no-root  \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . /backend

CMD ["sh", "-c", "cd src && alembic upgrade head && python main.py"]
