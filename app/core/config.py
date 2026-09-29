"""Configuração central do projeto.

Todos os valores vêm de variáveis de ambiente (arquivo .env).
Nenhuma credencial fica gravada no código.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Meu Dia"
    app_env: str = "development"

    db_host: str = ""
    db_port: int = 3306
    db_name: str = "agenda"
    db_user: str = ""
    db_password: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
