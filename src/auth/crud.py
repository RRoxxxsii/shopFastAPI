import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import RegisterUserIn
from src.models import User, Token


class BaseCrud:
    def __init__(self, session: AsyncSession):
        self.session = session


class BaseFindUser(BaseCrud):
    async def get_user_exists(self, email: str) -> [User | None]:
        statement = select(User).where(User.email == email)
        db_user = await self.session.execute(statement)
        db_user = db_user.scalar_one_or_none()
        return db_user


class CreateTokenCRUD(BaseFindUser):
    async def create_token(self, user: User) -> None:
        token = Token(user_id=user.id, access_token=str(uuid.uuid4()))
        self.session.add(token)


class RegisterUserCrud(BaseFindUser):

    async def create_user(self, user: RegisterUserIn, hashed_password: str):
        user = User(
            name=user.name, surname=user.surname, email=user.email, hashed_password=hashed_password
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user



