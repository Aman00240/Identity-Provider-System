from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PRIVATE_KEY: str = (BASE_DIR / "certs" / "private.pem").read_text()
    PUBLIC_KEY: str = (BASE_DIR / "certs" / "public.pem").read_text()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
