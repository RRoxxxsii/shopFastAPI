from httpx import AsyncClient
from starlette import status


class TestGetItem:
    async def test_get_item_by_id(self, ac: AsyncClient, user, token, category, item):
        response = await ac.get("/items/get-item/", headers={"Authorization": token}, params={"item_id": item.id})
        assert response.status_code == status.HTTP_200_OK

    async def test_get_item_by_id_does_not_exist(self, ac: AsyncClient, user, token, category, item):
        response = await ac.get("/items/get-item/", headers={"Authorization": token}, params={"item_id": item.id + 1})
        assert response.status_code == status.HTTP_404_NOT_FOUND
