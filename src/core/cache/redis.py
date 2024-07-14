import json
from dataclasses import dataclass
from datetime import timedelta
from redis import asyncio as aioredis
from redis.exceptions import ConnectionError
from redis.asyncio.retry import Retry
from redis.backoff import NoBackoff
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings


class RedisCache:
    """Cache service"""

    __connect: aioredis.Redis = aioredis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        max_connections=10_000,
        socket_connect_timeout=5.0,
        socket_keepalive=True,
        retry=Retry(NoBackoff(), 3),
        retry_on_error=[ConnectionError],
        health_check_interval=30,
    )

    @classmethod
    async def get(cls, key: str) -> Any:
        """Return the value at key `name`, or None if the key doesn't exist"""
        async with cls.__connect as connect:
            return await connect.get(key)

    @classmethod
    async def set(
        cls, key: str, value: Any, ttl: int | timedelta = 300
    ) -> None:
        """Set the value at key `name` to `value`"""
        async with cls.__connect as connect:
            await connect.set(key, value, ex=ttl)

    @classmethod
    async def clear(cls) -> None:
        """Delete all keys in all databases on the current host"""
        async with cls.__connect as connect:
            await connect.flushall()


@dataclass
class CacheData[ServiceT]:
    key: str
    model_id: int
    session: AsyncSession
    service: ServiceT


async def check_template_cache[SchemeT](
        cache_data: CacheData, validate_func: callable, *args, **kwargs
) -> SchemeT:
    """Sets template in the cache if it not already there"""

    value_from_cache = await RedisCache.get(cache_data.key)
    if value_from_cache is None:
        img = await cache_data.service.get_one(
            cache_data.session, cache_data.model_id
        )
        value: SchemeT = validate_func(img, *args, **kwargs)
        await RedisCache.set(cache_data.key, value.model_dump_json(), 5)
        return value

    if isinstance(value_from_cache, str | bytes):
        value_from_cache: SchemeT = validate_func(
            json.loads(value_from_cache.decode())
        )
    return value_from_cache
