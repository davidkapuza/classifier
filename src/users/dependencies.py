from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_async_session
from .service import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(session)
