from httpx import AsyncClient
from starlette import status


class TestUserRegister:
    async def test_register(self, ac: AsyncClient):
        response = await ac.post('/users/sign-up/', json={
          "name": "string",
          "surname": "string",
          "email": "user@example.com",
          "password1": "string",
          "password2": "string"
        }
                               )

        assert response.status_code == status.HTTP_201_CREATED

    async def test_register_passwords_dont_match(self, ac: AsyncClient):
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

    async def test_register_email_exists(self, ac: AsyncClient, user):
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


class TestLoginToken:

    async def test_create_token(self, ac: AsyncClient, user):
        response = await ac.post('/users/create-token/', json={
            'password': 'hashed+12345',
            'email': 'testuser@example.com'
        }
                                 )
        assert response.status_code == status.HTTP_200_OK

    async def test_create_token_user_not_provided(self, ac: AsyncClient):
        """
        User with provided credentials does not exist
        """
        response = await ac.post('/users/create-token/', json={
            'password': 'password',
            'email': 'testuser@example.com'
        }
                                 )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert eval(response.content.decode()) == {"detail": "User with provided credentials not found"}

    async def test_password_does_not_match(self, ac: AsyncClient, user):
        """
        Password does not match to the provided email
        """
        response = await ac.post('/users/create-token/', json={
            'password': 'password',
            'email': 'testuser@example.com'
        }
                                 )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert eval(response.content.decode()) == {"detail": "Incorrect password"}
