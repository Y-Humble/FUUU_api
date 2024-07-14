from httpx import AsyncClient, Response
from tests.builders import FakeMeme


async def test_create_meme(
    async_client: AsyncClient, images_ids: list[int]
) -> None:
    for img_id in images_ids:
        post_response: Response = await async_client.post(
            "/meme", json={"img_id": img_id, **FakeMeme().get_text()}
        )
        assert post_response.status_code == 201
        meme_id: dict[str, str] = post_response.json()["meme_id"]
        meme_response: Response = await async_client.get(f"/meme/{meme_id}")
        assert meme_response.status_code == 200


async def test_create_user_list_memes(async_client: AsyncClient) -> None:
    post_response: Response = await async_client.post(
        "/meme/user/list", json=FakeMeme().get_text()
    )
    assert post_response.status_code == 201
    for meme in post_response.json():
        meme_id: dict[str, str] = meme["meme_id"]
        meme_response: Response = await async_client.get(f"/meme/{meme_id}")
        assert meme_response.status_code == 200


async def test_create_list_memes(async_client: AsyncClient) -> None:
    post_response: Response = await async_client.post(
        "/meme/list", json=FakeMeme().get_text()
    )
    assert post_response.status_code == 201
    for meme in post_response.json():
        meme_id: dict[str, str] = meme["meme_id"]
        meme_response: Response = await async_client.get(f"/meme/{meme_id}")
        assert meme_response.status_code == 200
