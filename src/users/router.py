from fastapi import APIRouter, Depends, status, BackgroundTasks
from .dtos import CreateUserDto

from .dependencies import get_user_service

from .service import UserService

users_router = APIRouter()


@users_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    create_user_dto: CreateUserDto,
    bg_tasks: BackgroundTasks,
    users_service: UserService = Depends(get_user_service),
):
    user_exists = await users_service.get_user_by_email(create_user_dto.email)

    # TODO
