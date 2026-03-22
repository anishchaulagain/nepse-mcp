"""Application settings using pydantic-settings."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "NEPSE AI Prediction Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./nepse.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 300  # seconds

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Groq LLM
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # API
    API_V1_PREFIX: str = "/api/v1"
    CHUKUL_API_URL: str = "https://chukul.com/api/data/adjhistorydata/data/"
    CHUKUL_SYMBOL_API_URL: str = "https://chukul.com/api/data/symbol/"
    NEPALI_PAISA_API_URL: str = "https://nepalipaisa.com/api/GetStockDataForChart"

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
