from pydantic_settings import BaseSettings, SettingsConfigDict

from core.config.cors import CorsSettings
from core.config.run import RunSettings


class Settings(BaseSettings):
    """
    Application settings.
    run - host, port, app_title, log_level
    cors - origins, headers, methods
    """

    run: RunSettings
    cors: CorsSettings

    model_config = SettingsConfigDict(
        env_file=".env.local",
        extra="allow",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


settings: Settings = Settings()
