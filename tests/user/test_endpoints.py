from httpx import AsyncClient, Response

from tests.builders.user import FakeUser
from src.user import Status


async def test_register_user(async_client: AsyncClient) -> None:
    list_credentials = [FakeUser().get_data() for _ in range(10)]
    for credentials in list_credentials:
        register: Response = await async_client.post(
            "/user/register", json=credentials
        )
        assert register.status_code == 201
        user: dict = register.json()
        assert user["username"] == credentials["username"]
        assert user["email"] == credentials["email"]
        assert user["active"]
        assert user["status"] == Status.ENJOYER.value
