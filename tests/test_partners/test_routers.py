from httpx import AsyncClient
from pytest_mock import MockFixture
from starlette import status


class TestBecomePartnerExistsAccount:
    async def test_become_partner(self, ac: AsyncClient, mocker: MockFixture, user, token):

        mocker.patch(
            "src.infrastructure.api_client.partners.implementation.Client.execute", return_value=True
        )  # Mock Fake response

        response = await ac.post(
            "/partners/upgrade-to-partner/",
            json={
                "bic": "044525225",
                "tin": "381111467850",
                "trrc": "775001001",
                "mobile": "89086469507",
                "company_name": "A name",
                "company_description": "A description",
                "bank_name": "Bank name",
                "an": "783768329692",
            },
            headers={"Authorization": token},
        )
        assert response.status_code == status.HTTP_201_CREATED

    async def test_become_partner_api_validation_failed(self, ac: AsyncClient, mocker: MockFixture, user, token):
        """
        Credentials validation through API failed.
        """
        mocker.patch(
            "src.infrastructure.api_client.partners.implementation.Client.execute", return_value=False
        )  # Mock Fake response

        response = await ac.post(
            "/partners/upgrade-to-partner/",
            json={
                "bic": "0",
                "tin": "0",
                "trrc": "0",
                "mobile": "0",
                "company_name": "A name",
                "company_description": "A description",
                "bank_name": "Bank name",
                "an": "0",
            },
            headers={"Authorization": token},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_become_partner_credentials_exist(self, ac: AsyncClient, mocker: MockFixture, user, token, partner):
        """
        Credentials are not unique
        """

        mocker.patch(
            "src.infrastructure.api_client.partners.implementation.Client.execute", return_value=True
        )  # Mock Fake response

        response = await ac.post(
            "/partners/upgrade-to-partner/",
            json={
                "bic": "044525225",
                "tin": "381111467850",
                "trrc": "775001001",
                "mobile": "89086469507",
                "company_name": "A name",
                "company_description": "A description",
                "bank_name": "Bank name",
                "an": "783768329692",
            },
            headers={"Authorization": token},
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert eval(
            response.content.decode(),
            {"detail": "User with tin 381111467850 already exists"},
        )


class TestRegisterAsPartner:
    async def test_register(self, ac: AsyncClient, mocker: MockFixture):

        mocker.patch(
            "src.infrastructure.api_client.partners.implementation.Client.execute", return_value=True
        )  # Mock Fake response

        response = await ac.post(
            "/partners/register-as-partner/",
            json={
                "name": "string",
                "surname": "string",
                "email": "user@example.com",
                "password1": "string",
                "password2": "string",
                "bic": "044525225",
                "tin": "381111467850",
                "trrc": "775001001",
                "mobile": "89086469507",
                "company_name": "A name",
                "company_description": "A description",
                "bank_name": "Bank name",
                "an": "783768329692",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    async def test_become_partner_api_validation_failed(self, ac: AsyncClient, mocker: MockFixture, user, token):
        """
        Credentials validation through API failed.
        """
        mocker.patch(
            "src.infrastructure.api_client.partners.implementation.Client.execute", return_value=False
        )  # Mock Fake response

        response = await ac.post(
            "/partners/register-as-partner/",
            json={
                "name": "string",
                "surname": "string",
                "email": "user@example.com",
                "password1": "string",
                "password2": "string",
                "bic": "0",
                "tin": "0",
                "trrc": "0",
                "mobile": "0",
                "company_name": "A name",
                "company_description": "A description",
                "bank_name": "Bank name",
                "an": "0",
            },
            headers={"Authorization": token},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_become_partner_credentials_exist(self, ac: AsyncClient, mocker: MockFixture, user, token, partner):
        """
        Credentials are not unique
        """
        mocker.patch(
            "src.infrastructure.api_client.partners.implementation.Client.execute", return_value=True
        )  # Mock Fake response

        response = await ac.post(
            "/partners/register-as-partner/",
            json={
                "name": "string",
                "surname": "string",
                "email": "user@example.com",
                "password1": "string",
                "password2": "string",
                "bic": "044525225",
                "tin": "381111467850",
                "trrc": "775001001",
                "mobile": "89086469507",
                "company_name": "A name",
                "company_description": "A description",
                "bank_name": "Bank name",
                "an": "783768329692",
            },
            headers={"Authorization": token},
        )

        assert response.status_code == status.HTTP_409_CONFLICT


class TestCreateItem:
    async def test_create_item(self, ac: AsyncClient, user, token, partner, category):
        response = await ac.post(
            "/partners/create-item/",
            json={
                "title": "Iphone 15 Pro Max",
                "description": "Cool phone",
                "price": 1.2,
                "category_id": category.id,
                "data": '{"size": "42", "color": "red", "material": "leather"}',
            },
            headers={"Authorization": token},
        )
        assert response.status_code == status.HTTP_201_CREATED

    async def test_item_exits(self, ac: AsyncClient, user, token, partner, category, item):
        response = await ac.post(
            "/partners/create-item/",
            json={
                "title": "Nike",
                "description": "Cool shoes",
                "price": 1.2,
                "category_id": category.id,
                "data": '{"size": "42", "color": "red", "material": "leather"}',
            },
            headers={"Authorization": token},
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    async def test_category_does_not_exist(self, ac: AsyncClient, user, token, partner, category):
        response = await ac.post(
            "/partners/create-item/",
            json={
                "title": "Iphone 15 Pro Max",
                "description": "Cool phone",
                "price": 1.2,
                "category_id": category.id + 10,
                "data": '{"size": "42", "color": "red", "material": "leather"}',
            },
            headers={"Authorization": token},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_category_data_does_not_match(self, ac: AsyncClient, user, token, partner, category):
        response = await ac.post(
            "/partners/create-item/",
            json={
                "title": "Iphone 15 Pro Max",
                "description": "Cool phone",
                "price": 1.2,
                "category_id": category.id,
                "data": '{"size": "42", "color": "red", "material": "leather"}',
            },
            headers={"Authorization": token},
        )
        assert response.status_code == status.HTTP_201_CREATED
