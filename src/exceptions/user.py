from src.exceptions.base import DomainException


class UserExists(DomainException):
    pass


class UserNotFound(DomainException):
    pass


class PasswordIsNotCorrect(DomainException):
    pass
