from sqlmodel import select
from src.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)

        result = await self.session.exec(statement)

        user = result.first()

        return user
