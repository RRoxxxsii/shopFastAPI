from src.domain.shop.exceptions.base import DomainException


class ItemExists(DomainException):
    pass


class ItemDoesNotExists(DomainException):
    pass
