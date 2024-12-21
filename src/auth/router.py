from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from .dtos import (
    LoginDto,
    LoginResponseDto,
    ResetPasswordConfirmationDto,
    ResetPasswordDto,
)
from .dependencies import RefreshTokenBearer, AccessTokenBearer
from .errors import (
    UserAlreadyExists,
    InvalidCredentials,
    AccountNotVerified,
    InvalidVerificationToken,
    NotFound,
)
from src.user.service import UsersService
from src.user.dependencies import get_user_service
from src.user.dtos import CreateUserDto
from .utils import (
    create_confirmation_token,
    verify_password,
    sign_tokens,
    verify_confirmation_token,
)

from src.mail.service import MailService
from src.redis.service import RedisService

auth_router = APIRouter()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    create_user_dto: CreateUserDto,
    bg_tasks: BackgroundTasks,
    users_service: UsersService = Depends(get_user_service),
    mail_service: MailService = Depends(),
):
    user_email = create_user_dto.email

    user = await users_service.get_user_by_email(user_email)

    if user and user.is_verified:
        raise UserAlreadyExists()

    if not user:
        user = await users_service.create_user(create_user_dto)

    token = create_confirmation_token(email=user_email)

    bg_tasks.add_task(
        mail_service.send_confirmation_email, email=user_email, token=token
    )

    return user


@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginResponseDto
)
async def login(
    login_dto: LoginDto, users_service: UsersService = Depends(get_user_service)
):
    user = await users_service.get_user_by_email(login_dto.email)

    if not user or not verify_password(login_dto.password, user.password_hash):
        raise InvalidCredentials()

    if not user.is_verified:
        raise AccountNotVerified()

    tokens = sign_tokens(user.model_dump())

    return LoginResponseDto(
        **tokens,
        user=user,
    )


@auth_router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_user(
    token: str, users_service: UsersService = Depends(get_user_service)
):
    user_email = verify_confirmation_token(token)

    if not user_email:
        raise InvalidVerificationToken()

    user = await users_service.confirm_user(user_email)

    return user


@auth_router.get("/refresh")
async def refresh(
    token_data: dict = Depends(refresh_token_bearer),
    users_service: UsersService = Depends(get_user_service),
):
    user_email = token_data["user"]["email"]
    user = await users_service.get_user_by_email(user_email)

    if not user:
        raise NotFound()

    tokens = sign_tokens(user.model_dump())

    return LoginResponseDto(
        **tokens,
        user=user,
    )


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(
    token_data: dict = Depends(access_token_bearer),
    redis_service: RedisService = Depends(),
):
    jti = token_data["jti"]
    await redis_service.blocklist_token(token_jti=jti)


@auth_router.post("/reset-password")
async def reset_password(
    reset_password_dto: ResetPasswordDto,
    bg_tasks: BackgroundTasks,
    mail_service: MailService = Depends(),
):
    user_email = reset_password_dto.email

    token = create_confirmation_token(email=user_email)

    bg_tasks.add_task(
        mail_service.send_reset_password_email, email=user_email, token=token
    )

    return JSONResponse(content=None, status_code=status.HTTP_200_OK)


@auth_router.post("/reset-password-confirm/{token}")
async def reset_password_confirm(
    token: str,
    passwords: ResetPasswordConfirmationDto,
    users_service: UsersService = Depends(get_user_service),
):
    user_email = verify_confirmation_token(token)
    print(user_email)
    if not user_email:
        raise InvalidVerificationToken()

    user = await users_service.update_password(user_email, passwords.new_password)

    return user
