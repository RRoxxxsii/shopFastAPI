from httpx import AsyncClient
from starlette import status


class TestGetItem:
    async def test_get_item_by_id(self, ac: AsyncClient, item):
        response = await ac.get("/items/get-item/", params={"item_id": item.id})
        assert response.status_code == status.HTTP_200_OK

    async def test_get_item_by_id_does_not_exist(self, ac: AsyncClient, item):
        response = await ac.get("/items/get-item/", params={"item_id": item.id + 1})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_list_item(self, ac: AsyncClient, item, item2):
        response = await ac.get("/items/get-all-items/")
        assert response.status_code == status.HTTP_200_OK
