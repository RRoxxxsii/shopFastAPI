from fastapi import HTTPException
from starlette import status


class BaseResponse:
    @staticmethod
    def raise_409(message: str = 'User with these credentials already exists'):
        raise HTTPException(
            status.HTTP_409_CONFLICT, message
        )

    @staticmethod
    def raise_400(message: str = 'Credentials are not valid'):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, message
        )

    @staticmethod
    def raise_401(message: str = 'UNAUTHORIZED'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )

    @staticmethod
    def raise_404(message: str = 'Not found'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )
