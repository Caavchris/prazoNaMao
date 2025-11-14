from pydantic_settings import BaseSettings
from functools import lru_cache
import toml

class Settings(BaseSettings):
    cnj_base_url: str
    cnj_timeout: int

    class Config:
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Load settings from config.toml with caching"""
    config = toml.load("config.toml")
    return Settings(
        cnj_base_url=config['cnj']['base_url'],
        cnj_timeout=config['cnj']['timeout']
    )