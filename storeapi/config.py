from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False

class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")

@lru_cache()
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)