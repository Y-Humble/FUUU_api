from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from typing import AsyncGenerator

from core.cache import RedisCache
from core.db import db_sidekick


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await RedisCache.clear()
    logger.info("🚀🚀🚀 Graceful start!!! 🚀🚀🚀")

    yield

    logger.info("Waiting for application shutdown")
    await db_sidekick.dispose()
    logger.info("🪂🪂🪂 Graceful shutdown!!! 🪂🪂🪂")
