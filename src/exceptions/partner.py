from src.exceptions.base import DomainException


class SellerExists(DomainException):
    pass


class DataNotValid(DomainException):
    pass
