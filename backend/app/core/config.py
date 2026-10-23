from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: SecretStr | None = None
    resqnet_demo_mode: bool = False
    cors_origins: str = "https://resqnet-eight-psi.vercel.app"

    @property
    def effective_database_url(self) -> str | None:
        """Use configured PostgreSQL normally, with an explicit SQLite demo fallback."""
        if self.database_url is not None:
            return self.database_url.get_secret_value()
        if self.resqnet_demo_mode:
            return "sqlite+pysqlite:///./resqnet-demo.sqlite3"
        return None

    @property
    def allowed_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
