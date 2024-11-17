from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException

from .dtos import CreateUserDto, LoginDto
from .dependencies import get_user_service, get_mail_service
from .service import UserService
from .utils import create_confirmation_token, verify_password

from src.mail.service import MailService

users_router = APIRouter()


@users_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    create_user_dto: CreateUserDto,
    bg_tasks: BackgroundTasks,
    users_service: UserService = Depends(get_user_service),
    mail_service: MailService = Depends(get_mail_service),
):
    user_email = create_user_dto.email

    user = await users_service.get_user_by_email(user_email)

    if user is not None:
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists, and requires confirmation",
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    created_user = await users_service.create_user(create_user_dto)

    token = create_confirmation_token(email=user_email)

    bg_tasks.add_task(
        mail_service.send_confirmation_email, email=user_email, token=token
    )

    return created_user


@users_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_dto: LoginDto, users_service: UserService = Depends(get_user_service)
):
    user = await users_service.get_user_by_email(login_dto.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account doesn't exist, registration is required",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is in the process of registration, email confirmation is required",
        )

    password_valid = verify_password(login_dto.password, user.password_hash)

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )
    
    # TODO Tokens generation

