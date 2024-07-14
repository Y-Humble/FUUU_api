import pytest
from httpx import AsyncClient, Response

from tests.builders import FakeUser


@pytest.fixture(scope="package", autouse=True)
async def register_user_for_admin(async_client: AsyncClient) -> None:
    list_credentials: list[dict[str, str]] = [
        FakeUser().get_data() for _ in range(10)
    ]
    for credentials in list_credentials:
        register: Response = await async_client.post(
            "/users/register", json=credentials
        )
