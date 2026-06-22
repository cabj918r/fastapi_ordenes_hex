# app/infrastructure/adapters/database/settings.py
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    POSTGRES_USER: str = "programador_data"
    POSTGRES_PASSWORD: str = "password_seguro_123"
    POSTGRES_DB: str = "thelook_ecommerce"
    # Do not hardcode secrets. Provide `API_KEY_SECRET` via `.env` or environment variable.
    API_KEY_SECRET: str = ""
    API_KEY_SECRET_JWT: str = " "

    @property
    def DATABASE_URL(self) -> str:
        # Si Docker inyecta una URL completa, usamos esa.
        # Si no, la armamos dinámicamente apuntando a localhost agregando explícitamente el driver (+psycopg2).
        return os.getenv(
            "DATABASE_URL",
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:5432/{self.POSTGRES_DB}",
        )


# Instanciamos la configuración para poder importarla en el resto del proyecto
settings = Settings()
