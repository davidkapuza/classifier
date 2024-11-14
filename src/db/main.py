from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config

async_engine = create_async_engine(Config.DATABASE_URL, echo=True, future=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
