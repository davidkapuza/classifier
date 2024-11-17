from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_async_session
from .service import UserService
from src.mail.service import MailService


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(session)


async def get_mail_service() -> MailService:
    return MailService()
