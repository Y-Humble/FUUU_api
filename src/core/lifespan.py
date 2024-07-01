from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("🚀🚀🚀 Graceful start!!! 🚀🚀🚀")

    yield

    logger.info("Waiting for application shutdown")
    logger.info("🪂🪂🪂 Graceful shutdown!!! 🪂🪂🪂")
