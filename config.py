import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "data" / "db.sqlite3"


class DbConfig(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
    echo: bool = False
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


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
