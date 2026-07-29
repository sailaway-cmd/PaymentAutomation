"""Loads settings and secrets from environment variables (.env)."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    telegram_bot_token: str
    google_credentials_path: str
    google_sheet_id: str
    google_sheet_worksheet: str


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_config() -> Config:
    return Config(
        telegram_bot_token=_require("TELEGRAM_BOT_TOKEN"),
        google_credentials_path=_require("GOOGLE_CREDENTIALS_PATH"),
        google_sheet_id=_require("GOOGLE_SHEET_ID"),
        google_sheet_worksheet=os.getenv("GOOGLE_SHEET_WORKSHEET", "Sheet1"),
    )
