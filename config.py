import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "data" / "db.sqlite3"


class DbConfig(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
    echo: bool = False


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    dt_format: str = "%Y-%m-%d %H:%M:%S"


class Settings(BaseSettings):
    db: DbConfig = DbConfig()
    logger: LoggingConfig = LoggingConfig()


settings = Settings()
logging.basicConfig(
    level=settings.logger.level,
    format=settings.logger.format,
    datefmt=settings.logger.dt_format,
)
