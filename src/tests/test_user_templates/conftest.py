import pytest
from pathlib import Path
from httpx import AsyncClient

from apps.user.templates.services import UserTemplateService
from core.constants import Const


def delete_folder(path: Path) -> None:
    for sub in path.iterdir():
        if sub.is_file():
            sub.unlink()
        else:
            delete_folder(sub)
            sub.rmdir()


@pytest.fixture(scope="package", autouse=True)
async def set_and_clean_test_templates_dir(async_client: AsyncClient):
    templates_dir: Path = Const.TEST_USER_TEMPLATES_DIR
    UserTemplateService._path_to_templates = templates_dir
    yield
    for directory in templates_dir.iterdir():
        delete_folder(directory)
        directory.rmdir()
