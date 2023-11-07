import pytest
from httpx import AsyncClient
from sqlalchemy import select
from starlette import status

from src import models
from tests.conftest import async_session_maker


class TestBecomePartnerExistsAccount:

    async def test_become_partner(self, ac: AsyncClient, user, token):
        response = await ac.post('/partners/upgrade-to-seller/', json={
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
        response = await ac.post('/partners/upgrade-to-seller/', json={
            'bic': '0',
            'tin': '0',
            'trrc': '0',
            'mobile': '0',
            'company_name': 'A name',
            'company_description': 'A description',
            'bank_name': 'Bank name',
            'an': '0',
        }, headers={'Authorization': token})
        assert response.status_code == status.HTTP_409_CONFLICT

    async def test_become_partner_credentials_exist(self, ac: AsyncClient, user, token, seller):
        """
        Credentials are not unique
        """
        response = await ac.post('/partners/upgrade-to-seller/', json={
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
