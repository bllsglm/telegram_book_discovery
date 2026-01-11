"""Telegram public preview scraping."""

from __future__ import annotations

import logging
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

from .config import Config

logger = logging.getLogger(__name__)


def _get_meta_content(soup: BeautifulSoup, prop: str) -> str | None:
    tag = soup.find("meta", attrs={"property": prop})
    if not tag:
        return None
    content = tag.get("content")
    if not content:
        return None
    return content.strip()


def fetch_telegram_preview(handle: str, config: Config) -> Optional[Dict[str, str]]:
    """Fetch Telegram preview HTML and extract title and description."""
    url = f"https://t.me/{handle}"
    headers = {"User-Agent": config.telegram_preview_user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=config.request_timeout)
    except requests.RequestException as exc:
        logger.warning("Telegram preview request failed for %s: %s", handle, exc)
        return None

    if response.status_code != 200:
        logger.info("Telegram preview returned %s for %s", response.status_code, handle)
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ").lower()
    if "channel cannot be displayed" in page_text:
        return None

    title = _get_meta_content(soup, "og:title")
    description = _get_meta_content(soup, "og:description")
    if not title or not description:
        return None

    return {
        "handle": handle,
        "title": title,
        "description": description,
        "url": url,
    }
