from httpx import AsyncClient, Response
from core.constants import Const
from tests.builders.template import FakeTemplate


async def test_post_endpoint(
    async_client: AsyncClient, template_data: list[FakeTemplate]
) -> None:
    for template in template_data:
        post_response: Response = await async_client.post(
            "/user/template",
            files=template.get_files_data(Const.TEST_INTPUT_PATH),
            data=template.get_form_data(),
        )
        assert post_response.status_code == 201


async def test_get_endpoints(
    async_client: AsyncClient,
    template_data: list[FakeTemplate],
) -> None:
    list_response: Response = await async_client.get("/user/template/list")
    assert list_response.status_code == 200
    for val, template in zip(list_response.json(), template_data):
        assert val["title"] == template.title
        assert val["category"] == template.category
        assert isinstance(val["id"], int)
        val_id: int = val["id"]
        get_id_response: Response = await async_client.get(
            f"/user/template/{val_id}",
        )
        assert get_id_response.status_code == 200


async def test_patch_endpoint(
    async_client: AsyncClient,
    template_data: list[FakeTemplate],
) -> None:
    for val_id, template in enumerate(template_data, 1):
        changed_template: FakeTemplate = template.new_form_data()
        patch_response = await async_client.patch(
            f"/user/template/{val_id}",
            json=changed_template.get_form_data(),
        )
        assert patch_response.status_code == 200
        patch_response = patch_response.json()
        assert patch_response["title"] == changed_template.title + ".jpg"
        assert patch_response["category"] == changed_template.category


async def test_put_endpoint(
    async_client: AsyncClient,
    template_data: list[FakeTemplate],
) -> None:
    for val_id, template in enumerate(template_data, 1):
        changed_template: FakeTemplate = template.new_form_data()
        put_response = await async_client.put(
            f"/user/template/{val_id}",
            json=changed_template.get_form_data(),
        )
        assert put_response.status_code == 200
        put_response = put_response.json()
        assert put_response["title"] == changed_template.title + ".jpg"
        assert put_response["category"] == changed_template.category


async def test_delete_endpoint(async_client: AsyncClient):
    list_response: Response = await async_client.get("/user/template/list")
    for val in list_response.json():
        delete_response = await async_client.delete(
            f"/user/template/{val["id"]}",
        )
        assert delete_response.status_code == 204
