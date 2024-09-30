from typing import Literal, Optional
from pydantic_settings import BaseSettings  
from pydantic import model_validator

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: Optional[str] = None

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    TEST_DATABASE_URL: Optional[str] = None

    SECRET_KEY: str
    ALGORITHM: str

    @model_validator(mode="after")
    def get_database_url(cls, values):
        values.DATABASE_URL = f"postgresql+asyncpg://{values.DB_USER}:{values.DB_PASS}@{values.DB_HOST}:{values.DB_PORT}/{values.DB_NAME}"
        return values

    @model_validator(mode="after")
    def get_test_database_url(cls, values):
        values.TEST_DATABASE_URL = f"postgresql+asyncpg://{values.TEST_DB_USER}:{values.TEST_DB_PASS}@{values.TEST_DB_HOST}:{values.TEST_DB_PORT}/{values.TEST_DB_NAME}"
        return values

    class Config:
        env_file = '.env'

settings = Settings()
print(settings.dict())
print(settings.DATABASE_URL)

# Arguments missing for parameters "MODE", "DB_HOST", "DB_PORT", "DB_USER", "DB_PASS", "DB_NAME", "TEST_DB_HOST", "TEST_DB_PORT", "TEST_DB_USER", "TEST_DB_PASS", "TEST_DB_NAME", "SECRET_KEY", "ALGORITHM"