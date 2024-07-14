from pydantic import BaseModel


class RedisSettings(BaseModel):
    host: str
    port: int