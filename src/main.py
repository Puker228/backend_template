import uvicorn
from fastapi import FastAPI, HTTPException
from loguru import logger
from redis.asyncio import Redis

from config import settings
from user.schema import UserSchema

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@app.post("/add_name")
async def add_name(name_model: UserSchema):
    logger.info("Adding name to Redis")
    await redis.set("name", name_model.name)
    return {"message": f"Name '{name_model.name}' added to Redis."}


@app.get("/names")
async def get_name():
    logger.info("Retrieving name from Redis")
    name = await redis.get("name")
    if name is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return {"name": name.decode("utf-8")}  # Декодируем байты в строку


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
