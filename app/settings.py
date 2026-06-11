from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Event Management API"
    app_version: str = "0.1.0"
    debug: bool = False
    allowed_hosts: list[str] = ["*"]

    # Base de données
    database_url: str

    # Sécurité JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
