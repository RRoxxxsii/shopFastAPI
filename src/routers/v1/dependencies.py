from typing import Annotated

from fastapi import Depends

from src.api.partners.client import AbstractAPIClient, Client
from src.database.uow import AbstractUnitOfWork, UnitOfWork

UOWDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]

APIClientDep = Annotated[AbstractAPIClient, Depends(Client)]
