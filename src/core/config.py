from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

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
