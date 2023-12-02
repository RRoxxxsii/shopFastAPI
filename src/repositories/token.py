from src.models.auth import Token
from src.repositories.base import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    model = Token
