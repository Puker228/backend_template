import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

current_date = datetime.now().strftime("%Y-%m-%d")

BASE_DIR = Path(__file__).resolve().parent.parent.parent / "src/project_logs"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(
    LOG_DIR / f"{current_date}.log",
    format="{time}-{level}-{message} | {process} | {thread} | {file.path}:{name}:{function}:{line}",
    level="INFO",
    rotation="1 day",
    compression="zip",
    retention="10 days",
    enqueue=True,
)
logger.add(
    sys.stderr,
    format="{time}-{level}-{message} | {process} | {thread} | {file.path}:{name}:{function}:{line}",
    level="INFO",
    enqueue=True,
)
