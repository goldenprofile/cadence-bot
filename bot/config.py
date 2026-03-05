from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    db_path: Path


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set in environment")

    db_path = Path(os.getenv("DB_PATH", "data/cadence.db"))
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return Config(bot_token=token, db_path=db_path)
