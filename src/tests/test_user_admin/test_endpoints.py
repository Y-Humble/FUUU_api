from httpx import AsyncClient, Response

from apps.user.messages import UserResponseMessage
from apps.user.models import Status
from tests.builders import FakeUser


type UserT = dict[str, str | True]


async def test_get_users_list(async_client: AsyncClient) -> None:
    list_user: Response = await async_client.get("/user/admin/list")
    assert list_user.status_code == 200
    users: list[UserT] = list_user.json()
    assert len(users) > 0
    set_rows: set[str] = {"username", "email", "id", "active", "status"}
    for user in users:
        assert set_rows == set(user)


async def test_ban_user(async_client: AsyncClient) -> None:
    list_user: Response = await async_client.get("/user/admin/list")
    users: list[UserT] = list_user.json()
    user_indx: int = 5
    user = users[user_indx]
    user_id: str = user["id"]
    ban_user: Response = await async_client.post(
        "/user/admin/ban", params={"user_id": user_id}
    )
    response: dict[str, str] = ban_user.json()
    assert ban_user.status_code == 200
    assert response == UserResponseMessage.BANNED_USER

    banned_user_response: Response = await async_client.get(
        f"/user/admin/user/{user_id}"
    )
    banned_user: UserT = banned_user_response.json()
    assert banned_user["status"] == Status.BANNED.value


async def test_get_user_by_username(async_client: AsyncClient) -> None:
    list_user: Response = await async_client.get("/user/admin/list")
    users: list[UserT] = list_user.json()
    user_indx: int = 5
    user = users[user_indx]
    username: str = user["username"]
    user_response: Response = await async_client.get(
        f"/user/admin/user-username/{username}"
    )
    assert user_response.status_code == 200


async def test_get_user_by_email(async_client: AsyncClient) -> None:
    list_user: Response = await async_client.get("/user/admin/list")
    users: list[UserT] = list_user.json()
    user_indx: int = 5
    user = users[user_indx]
    email: str = user["email"]
    user_response: Response = await async_client.get(
        f"/user/admin/user-email/{email}"
    )
    assert user_response.status_code == 200


async def test_get_user_by_id(async_client: AsyncClient) -> None:
    list_user: Response = await async_client.get("/user/admin/list")
    users: list[UserT] = list_user.json()
    user_indx: int = 5
    user = users[user_indx]
    user_id: str = user["id"]
    user_response: Response = await async_client.get(
        f"/user/admin/user/{user_id}"
    )
    assert user_response.status_code == 200


async def test_update_user(async_client: AsyncClient) -> None:
    list_user: Response = await async_client.get("/user/admin/list")
    users: list[UserT] = list_user.json()
    user_indx: int = 5
    user = users[user_indx]
    user_id: str = user["id"]
    list_new_data = [FakeUser().get_data() for _ in range(10)]
    for new_data in list_new_data:
        current_user: Response = await async_client.put(
            f"/user/admin/user/{user_id}", json=new_data
        )
        assert current_user.status_code == 200
        user: dict = current_user.json()
        assert user["username"] == new_data["username"]
        assert user["email"] == new_data["email"]


async def test_delete_user(async_client: AsyncClient) -> None:
    list_user: Response = await async_client.get("/user/admin/list")
    users: list[UserT] = list_user.json()
    user = users[5]
    user_id: str = user["id"]
    deleted_user: Response = await async_client.delete(
        f"/user/admin/user/{user_id}"
    )
    assert deleted_user.status_code == 200
    assert deleted_user.json() == UserResponseMessage.DELETED_USER
