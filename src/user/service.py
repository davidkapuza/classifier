from sqlmodel import select
from src.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from .dtos import CreateUserDto
from src.auth.utils import get_password_hash


class UsersService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        result = await self.session.execute(statement)

        user = result.scalar_one_or_none()

        return user

    async def create_user(self, create_user_dto: CreateUserDto) -> User:
        user_dict = create_user_dto.model_dump()

        new_user = User(**user_dict)

        new_user.password_hash = get_password_hash(user_dict["password"])

        self.session.add(new_user)

        await self.session.commit()

        return new_user

    async def confirm_user(self, email: str) -> User:
        user = await self.get_user_by_email(email)

        if not user:
            raise Exception("User not found")

        user.is_verified = True

        await self.session.commit()

        return user
