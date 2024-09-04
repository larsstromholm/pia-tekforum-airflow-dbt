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


settings = Settings()
