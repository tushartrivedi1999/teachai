from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Rivinity Learning API"
    app_version: str = "0.1.0"
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./rivinity.db"
    mistral_api_key: str | None = None
    mistral_model: str = "mistral-large-latest"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
