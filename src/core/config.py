from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_HOST: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_NAME: str

    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        title="Book management",
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )


Config: Settings = Settings()
