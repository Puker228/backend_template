#!/bin/sh
set -e
cd src

echo "Running migrations..."
alembic upgrade head

echo "Starting server..."
exec python main.py
