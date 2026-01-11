"""Configuration loading for tg_discovery."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Iterable, List

from dotenv import load_dotenv

# Telegram preview için makul bir User-Agent
DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Türkçe kitap / ekitap / sınav kitapları odaklı default sorgular
DEFAULT_QUERIES = [
    # Genel Türkçe kitap arşivleri
    "telegram türkçe kitap pdf",
    "telegram türkçe pdf kitap arşivi",
    "telegram türkçe kitap arşivi",
    "telegram ekitap arşivi",
    "telegram e kitap pdf",
    "telegram roman pdf arşiv",
    "telegram felsefe kitap pdf",
    "telegram edebiyat kitap pdf",

    # KPSS / YKS / sınav kitapları
    "telegram kpss kitap pdf",
    "telegram kpss pdf kitap arşivi",
    "telegram yks kitap pdf",
    "telegram tyt kitap pdf",
    "telegram ayt kitap pdf",
    "telegram dgs kitap pdf",
    "telegram ales kitap pdf",
    "telegram yds pdf kitap",

    # Ders notu / çıkmış soru
    "telegram ders notu pdf",
    "telegram çıkmış soru pdf",
    "telegram çıkmış sorular kitap pdf",

    # Sesli kitap vs. (csv'de var)
    "telegram sesli kitap pdf",
]


@dataclass(frozen=True)
class Config:
    """Configuration values loaded from environment."""

    google_api_key: str
    google_cse_cx: str
    default_queries: List[str]
    max_pages_per_query: int
    request_timeout: int
    telegram_preview_user_agent: str


def _parse_list_env(value: str | None, fallback: Iterable[str]) -> List[str]:
    """Parse a comma-separated env var into a list, or use fallback."""
    if not value:
        return list(fallback)
    parts = [item.strip() for item in value.split(",")]
    return [item for item in parts if item]


def _parse_int_env(value: str | None, fallback: int) -> int:
    """Parse an int env var with fallback on error."""
    if not value:
        return fallback
    try:
        return int(value)
    except ValueError:
        return fallback


def load_config() -> Config:
    """Load config from environment variables and .env file."""
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    cse_cx = os.getenv("GOOGLE_CSE_CX")
    if not api_key or not cse_cx:
        raise ValueError("Missing required env vars: GOOGLE_API_KEY, GOOGLE_CSE_CX")

    default_queries = _parse_list_env(os.getenv("DEFAULT_QUERIES"), DEFAULT_QUERIES)
    max_pages = _parse_int_env(os.getenv("MAX_PAGES_PER_QUERY"), 3)
    request_timeout = _parse_int_env(os.getenv("REQUEST_TIMEOUT"), 10)
    ua = os.getenv("TELEGRAM_PREVIEW_USER_AGENT", DEFAULT_UA)

    return Config(
        google_api_key=api_key,
        google_cse_cx=cse_cx,
        default_queries=default_queries,
        max_pages_per_query=max_pages,
        request_timeout=request_timeout,
        telegram_preview_user_agent=ua,
    )
