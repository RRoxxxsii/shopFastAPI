from src.services.user import CreateUserService
from src.repositories.user import UserRepository
from src.secure.pwd import PwdImpl


def create_user_service():
    return CreateUserService(UserRepository, PwdImpl)
