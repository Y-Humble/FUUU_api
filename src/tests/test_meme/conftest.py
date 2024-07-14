import pytest
from pathlib import Path
from httpx import AsyncClient, Response

from apps.meme.templates import MemeTemplateService
from core.constants import Const
from tests.builders import FakeTemplate


@pytest.fixture(scope="package", autouse=True)
async def set_and_clean_test_templates_dir(async_client: AsyncClient) -> None:
    templates_dir: Path = Const.TEST_TEMPLATES_DIR
    MemeTemplateService._path_to_templates = templates_dir
    yield
    for directory in templates_dir.iterdir():
        if directory.name != "users":
            for file in directory.iterdir():
                file.unlink()
            directory.rmdir()


@pytest.fixture(scope="package", autouse=True)
async def load_images(
    async_client: AsyncClient, template_data: list[FakeTemplate]
) -> None:
    for template in template_data:
        await async_client.post(
            "/meme/template",
            files=template.get_files_data(Const.TEST_INTPUT_PATH),
            data=template.get_form_data(),
        )

    for template in template_data:
        await async_client.post(
            "/user/template",
            files=template.get_files_data(Const.TEST_INTPUT_PATH),
            data=template.get_form_data(),
        )


@pytest.fixture(scope="package")
async def images_ids(async_client: AsyncClient) -> list[int]:
    list_response: Response = await async_client.get("/meme/template/list")
    return [response["id"] for response in list_response.json()]
