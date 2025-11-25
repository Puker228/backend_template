from faststream.rabbit.fastapi import RabbitRouter

from core.config import settings

bot_router = RabbitRouter(
    url=f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}@rabbitmq:5672/",
    prefix="/api",
)
