from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_URL: str

    DATABASE_URL: str

    AUTH_JWT_ALGORITHM: str
    AUTH_JWT_SECRET: str
    AUTH_JWT_TOKEN_EXPIRES_IN: int
    AUTH_REFRESH_SECRET: str
    AUTH_REFRESH_TOKEN_EXPIRES_IN: int
    AUTH_CONFIRMATION_SECRET: str
    AUTH_CONFIRMATION_EXPIRES: int

    REDIS_URL: str = "redis://localhost:6379/0"

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
