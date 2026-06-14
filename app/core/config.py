from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/aegis_db"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/aegis_db"
    # JWT
    JWT_SECRET_KEY: str = "hackathon-secret-key"
    SECRET_KEY: str = "hackathon-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # LLM
    LLM_PROVIDER: str = "qwen"
    AMD_API_URL: str = "http://localhost:8000"
    AMD_API_KEY: str = "abc-123"
    AMD_MODEL: str = "Qwen/Qwen2-7B-Instruct"
    # App
    APP_ENV: str = "development"
    APP_PORT: int = 8002

settings = Settings()
