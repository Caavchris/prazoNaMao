from pydantic_settings import BaseSettings
from functools import lru_cache
import toml

class Settings(BaseSettings):
    cnj_base_url: str
    cnj_timeout: int
    deadlines: dict = {}
    deadlines_default: int = 10
    deadlines_threshold: int = 3

    class Config:
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Load settings from config.toml with caching"""
    config = toml.load("config.toml")
    dl = config.get('deadlines', {})
    # Extract defaults
    default = dl.get('default', 10)
    threshold = dl.get('threshold', 3)
    # Build per-type map excluding default/threshold
    per_type = {k: v for k, v in dl.items() if k not in ('default', 'threshold')}
    return Settings(
        cnj_base_url=config['cnj']['base_url'],
        cnj_timeout=config['cnj']['timeout'],
        deadlines=per_type,
        deadlines_default=default,
        deadlines_threshold=threshold
    )