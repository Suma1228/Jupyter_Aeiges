from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://aegis:aegis_password@localhost:5432/aegis_db"
    DATABASE_URL_SYNC: str = "postgresql://aegis:aegis_password@localhost:5432/aegis_db"

    # JWT
    JWT_SECRET_KEY: str = "aegis-dev-secret-key-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # LLM
    LLM_PROVIDER: str = "mock"

    # App
    APP_ENV: str = "development"
    APP_PORT: int = 8000


settings = Settings()
