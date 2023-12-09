from src.infrastructure.database.models.auth import Token
from src.infrastructure.database.repositories.base import SQLAlchemyRepository
from src.infrastructure.database.repositories.token.interface import (
    AbstractTokenRepository,
)


class TokenRepository(AbstractTokenRepository, SQLAlchemyRepository):
    model = Token
