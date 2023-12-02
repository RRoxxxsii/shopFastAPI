from src.infrastructure.database.repositories.auth import TokenRepository, UserRepository
from src.services.auth import TokenService, UserService


def token_service():
    return TokenService(token_repo=TokenRepository, user_repo=UserRepository)


def user_service():
    return UserService(UserRepository)
