from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_M: int
    REFRESH_TOKEN_EXPIRE_D: int
    REDIS_HOST: str
    REDIS_PORT: int
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    API_PREFIX: str = "/api/v1"

    @property
    def database_url(self):
        return self.DATABASE_URL

    model_config = SettingsConfigDict(
        title="Book management",
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )


Config: Settings = Settings()
