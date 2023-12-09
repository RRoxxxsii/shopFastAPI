from src.infrastructure.database.models.auth import Token
from src.infrastructure.database.repositories.base import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    model = Token
