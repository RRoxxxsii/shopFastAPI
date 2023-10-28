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
