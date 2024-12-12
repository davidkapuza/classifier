from fastapi import APIRouter, Depends, status

from src.auth.dependencies import AccessTokenBearer
from src.user.service import UsersService
from src.user.dependencies import get_user_service

users_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@users_router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(
    token_data: dict = Depends(access_token_bearer),
    users_service: UsersService = Depends(get_user_service),
):
    user_email = token_data["user"]["email"]
    user = await users_service.get_user_by_email(user_email)
    return user
