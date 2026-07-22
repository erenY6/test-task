from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    GROQ_API_KEY: str = ""
    GROQ_BASE_URL: str = ""
    GROQ_MODEL: str = ""

    OWNER_EMAIL: str = ""

    CORS_ORIGINS: str = ""

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    RATE_LIMIT: int = 5


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()