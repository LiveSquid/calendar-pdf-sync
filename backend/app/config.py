"""App configuration, loaded from environment variables / .env.

TODO: define a pydantic-settings BaseSettings class with at least:
  - anthropic_api_key: str
  - google_client_secret_path: str
  - database_url: str (default to a local sqlite file)
See .env.example at the repo root for the expected variable names.
"""


from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", env_file_encoding="utf-8")

    anthropic_api_key: str
    google_client_secret_path: Path = BACKEND_DIR / "client_secret.json"
    database_url: str = f"sqlite:///{(BACKEND_DIR / 'app.db').as_posix()}"


settings = Settings()