from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.core.db import Base, db_sidekick
from src.main import app


@pytest.fixture(scope="session", autouse=True)
async def create_tables() -> AsyncGenerator[None, None]:
    async with db_sidekick._engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with db_sidekick._engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    test_app: FastAPI = app()
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as async_client:
        yield async_client
