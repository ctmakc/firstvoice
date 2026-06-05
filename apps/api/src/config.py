from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "FirstVoice API"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://fv:devpass@postgres:5432/firstvoice"
    sync_database_url: str = "postgresql://fv:devpass@postgres:5432/firstvoice"

    redis_url: str = "redis://redis:6379/0"

    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "firstvoice"
    minio_secret_key: str = "devpass123"
    minio_bucket: str = "recordings"
    minio_secure: bool = False

    nextauth_secret: str = "change-me-in-production"
    nextauth_url: str = "http://localhost:3000"

    gemini_api_key: str = ""

    polygon_rpc: str = "https://rpc-amoy.polygon.technology"
    provenance_contract_address: str = ""
    relayer_private_key: str = ""

    rate_limit_per_minute: int = 60
    max_upload_size_mb: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
