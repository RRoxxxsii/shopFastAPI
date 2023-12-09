from httpx import AsyncClient
from starlette import status


class TestBecomePartnerExistsAccount:

    async def test_become_partner(self, ac: AsyncClient, user, token):
        response = await ac.post('/partners/upgrade-to-partner/', json={
            'bic': '044525225',
            'tin': '381111467850',
            'trrc': '775001001',
            'mobile': '89086469507',
            'company_name': 'A name',
            'company_description': 'A description',
            'bank_name': 'Bank name',
            'an': '783768329692',
        }, headers={'Authorization': token})

        assert response.status_code == status.HTTP_201_CREATED

    async def test_become_partner_api_validation_failed(self, ac: AsyncClient, user, token):
        """
        Credentials validation through API failed.
        """
        response = await ac.post('/partners/upgrade-to-partner/', json={
            'bic': '0',
            'tin': '0',
            'trrc': '0',
            'mobile': '0',
            'company_name': 'A name',
            'company_description': 'A description',
            'bank_name': 'Bank name',
            'an': '0',
        }, headers={'Authorization': token})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_become_partner_credentials_exist(self, ac: AsyncClient, user, token, seller):
        """
        Credentials are not unique
        """
        response = await ac.post('/partners/upgrade-to-partner/', json={
            'bic': '044525225',
            'tin': '381111467850',
            'trrc': '775001001',
            'mobile': '89086469507',
            'company_name': 'A name',
            'company_description': 'A description',
            'bank_name': 'Bank name',
            'an': '783768329692',
        }, headers={'Authorization': token})

        assert response.status_code == status.HTTP_409_CONFLICT
        assert eval(response.content.decode(), {"detail": "User with tin 381111467850 already exists"})


class TestRegisterAsPartner:

    async def test_register(self, ac: AsyncClient):
        response = await ac.post('/partners/register-as-partner/', json={
           "name": "string",
           "surname": "string",
           "email": "user@example.com",
           "password1": "string",
           "password2": "string",
           'bic': '044525225',
           'tin': '381111467850',
           'trrc': '775001001',
           'mobile': '89086469507',
           'company_name': 'A name',
           'company_description': 'A description',
           'bank_name': 'Bank name',
           'an': '783768329692',
        })

        assert response.status_code == status.HTTP_201_CREATED

    async def test_become_partner_api_validation_failed(self, ac: AsyncClient, user, token):
        """
        Credentials validation through API failed.
        """
        response = await ac.post('/partners/register-as-partner/', json={
            "name": "string",
            "surname": "string",
            "email": "user@example.com",
            "password1": "string",
            "password2": "string",
            'bic': '0',
            'tin': '0',
            'trrc': '0',
            'mobile': '0',
            'company_name': 'A name',
            'company_description': 'A description',
            'bank_name': 'Bank name',
            'an': '0',
        }, headers={'Authorization': token})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_become_partner_credentials_exist(self, ac: AsyncClient, user, token, seller):
        """
        Credentials are not unique
        """
        response = await ac.post('/partners/register-as-partner/', json={
            "name": "string",
            "surname": "string",
            "email": "user@example.com",
            "password1": "string",
            "password2": "string",
            'bic': '044525225',
            'tin': '381111467850',
            'trrc': '775001001',
            'mobile': '89086469507',
            'company_name': 'A name',
            'company_description': 'A description',
            'bank_name': 'Bank name',
            'an': '783768329692',
        }, headers={'Authorization': token})

        assert response.status_code == status.HTTP_409_CONFLICT
