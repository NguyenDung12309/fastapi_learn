from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_M: int
    REFRESH_TOKEN_EXPIRE_D: int
    
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
