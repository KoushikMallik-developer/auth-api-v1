from pathlib import Path
from pydantic_settings import BaseSettings

# env_path = Path(".") / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str

    # JWT
    JWT_SECRET: str = (
        "709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = Path(".") / ".env"
