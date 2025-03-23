from datetime import datetime

from loguru import logger

current_date = datetime.now().strftime("%Y-%m-%d")

logger.add(
    f"logs/{current_date}.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="1 day",
    compression="zip",
    retention="10 days",
)
