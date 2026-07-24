"""Centralized, environment-driven application configuration."""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///data/job_market.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))
    scraper_delay_seconds: float = float(os.getenv("SCRAPER_DELAY_SECONDS", "1.5"))
    user_agent: str = os.getenv("USER_AGENT", "PakistanJobMarketIntelligence/1.0")

settings = Settings()
