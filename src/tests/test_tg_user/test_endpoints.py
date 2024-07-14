from httpx import AsyncClient, Response
from tests.builders.tg_user import FakeTgUser


user: FakeTgUser = FakeTgUser()


async def test_register_and_get_tg_user(async_client: AsyncClient) -> None:
    response: Response = await async_client.post(
        "/user/tg/register", json=user.get_data()
    )
    assert response.status_code == 201
    assert "tg_id" in response.json()
    assert "user_email" in response.json()
    assert "password" not in response.json()

    tg_id = response.json()["tg_id"]
    response: Response = await async_client.get(f"/user/tg/id/{tg_id}")
    assert response.status_code == 200
    assert "tg_id" in response.json()
    assert "user_email" in response.json()
