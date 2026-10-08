from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Meu Dia"
    app_env: str = "development"

    db_host: str = ""
    db_port: int = 3306
    db_name: str = "agenda"
    db_user: str = ""
    db_password: str = ""

    jwt_secret: str = Field(min_length=32)
    jwt_expira_minutos: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()