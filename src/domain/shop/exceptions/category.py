from src.domain.shop.exceptions.base import DomainException


class CategoryDataDoesNotMatch(DomainException):
    pass


class CategoryDoesNotExist(DomainException):
    pass
