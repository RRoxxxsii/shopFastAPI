from httpx import AsyncClient
from starlette import status


async def test_register(ac: AsyncClient):
    response = await ac.post('/users/sign-up/', json={
      "name": "string",
      "surname": "string",
      "email": "user@example.com",
      "password1": "string",
      "password2": "string"
    }
                           )

    assert response.status_code == status.HTTP_201_CREATED


async def test_register_passwords_dont_match(ac: AsyncClient):
    """
    Passwords are different
    """
    response = await ac.post('/users/sign-up/', json={
      "name": "string",
      "surname": "string",
      "email": "user@example.com",
      "password1": "string2",
      "password2": "string"
    }
                           )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_register_email_exists(ac: AsyncClient, user):
    """
    User is not created, because user with this email already exists.
    """
    response = await ac.post('/users/sign-up/', json={
      "name": "string",
      "surname": "string",
      "email": "testuser@example.com",
      "password1": "string",
      "password2": "string"
    }
                           )
    assert eval(response.content.decode()) == {"detail": "User with email testuser@example.com already exists"}
    assert response.status_code == status.HTTP_409_CONFLICT
