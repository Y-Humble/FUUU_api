from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.config.database import DBSettings
from core.config.cors import CorsSettings
from core.config.run import RunSettings

type ModeT = Literal["DEV", "PROD"]


class Settings(BaseSettings):
    """
    Application settings.
    run - host, port, app_title, log_level
    cors - origins, headers, methods
    db - driver, host, port, user, name, password,
        echo, echo_pool, pool_size, max_overflow
    """

    db: DBSettings
    run: RunSettings
    cors: CorsSettings

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


class SettingsFactory(BaseSettings):
    """
    Returns a config instance depending on the MODE variable in the .env
    mode - DEV, PROD
    """

    mode: ModeT
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    def __call__(self):
        if self.mode == "PROD":
            return Settings(_env_file=".env.prod")
        elif self.mode == "DEV":
            return Settings(_env_file=".env.dev")


settings: Settings = SettingsFactory()()
