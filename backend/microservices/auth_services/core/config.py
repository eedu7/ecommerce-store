from pathlib import Path

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


class Config(BaseConfig):
    POSTGRES_URL: str
    TEST_POSTGRES_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRE_DAYS_IN_MINUTES: int = 60 * 24 * 7  # 7 days
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str


config: Config = Config()
