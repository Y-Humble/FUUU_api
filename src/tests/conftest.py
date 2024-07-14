import os
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from apps.user.dependencies import get_user_admin
from builders.user import FakeUser
from core.constants import Const
from core.db.base import Base
from core.db.sidekick import db_sidekick
from core.setup import setup_app
from tests.builders import FakeTemplate


@pytest.fixture(scope="session", autouse=True)
async def create_tables() -> AsyncGenerator[None, None]:
    async with db_sidekick._engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with db_sidekick._engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


def override_get_user_admin() -> bool:
    return True


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    test_app: FastAPI = setup_app()
    test_app.dependency_overrides[get_user_admin] = override_get_user_admin
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.fixture(autouse=True)
async def register_and_login(async_client: AsyncClient):
    credentials = FakeUser().get_data()
    await async_client.post("/user/register", json=credentials)
    del credentials["email"]
    await async_client.post("user/auth/login", data=credentials)


@pytest.fixture(scope="session")
def template_data() -> list[FakeTemplate]:
    root, _, filenames = next(os.walk(Const.TEST_INTPUT_PATH))
    return [FakeTemplate(filename) for filename in filenames]
