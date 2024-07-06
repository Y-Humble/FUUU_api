from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from typing import AsyncGenerator


from core.db import Base, db_sidekick
from user import User


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with db_sidekick._engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("🚀🚀🚀 Graceful start!!! 🚀🚀🚀")

    yield

    logger.info("Waiting for application shutdown")
    await db_sidekick.dispose()
    logger.info("🪂🪂🪂 Graceful shutdown!!! 🪂🪂🪂")
