from fastapi import APIRouter

from user.schemas import UserSchema

user_router = APIRouter()


@user_router.get("/")
async def index(user: UserSchema):
    return {"message": f"Hello {user.name}"}
