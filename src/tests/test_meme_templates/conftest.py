import pytest
from pathlib import Path
from httpx import AsyncClient

from apps.meme.templates import MemeTemplateService
from core.constants import Const


@pytest.fixture(scope="package", autouse=True)
async def set_and_clean_test_templates_dir(async_client: AsyncClient):
    templates_dir: Path = Const.TEST_TEMPLATES_DIR
    MemeTemplateService._path_to_templates = templates_dir
    yield
    for directory in templates_dir.iterdir():
        if directory.name != "users":
            for file in directory.iterdir():
                file.unlink()
            directory.rmdir()
