from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Project settings."""

    postgres_host: str
    postgres_db: str
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    dbt_project_dir: Path
    dbt_profiles_dir: Path

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
