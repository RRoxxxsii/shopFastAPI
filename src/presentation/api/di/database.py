from src.infrastructure.database import async_session_maker
from src.infrastructure.database.uow import UnitOfWork


def get_sqlalchemy_uow():
    return UnitOfWork(async_session_maker)


# UOWDep = Annotated[AbstractUnitOfWork, Depends(get_sqlalchemy_uow)]
#
# APIClientDep = Annotated[AbstractAPIClient, Depends(Client)]
