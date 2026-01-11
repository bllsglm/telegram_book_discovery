"""Utility helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlparse


def extract_handle_from_url(url: str) -> str | None:
    """Extract a Telegram handle from a t.me URL."""
    if not url:
        return None

    try:
        parsed = urlparse(url)
    except ValueError:
        return None

    if "t.me" not in parsed.netloc:
        return None

    path = parsed.path.strip("/")
    if not path:
        return None

    parts = path.split("/")
    if parts[0].startswith("+") or parts[0] == "joinchat":
        return None

    if parts[0] == "s":
        if len(parts) < 2:
            return None
        handle = parts[1]
    elif parts[0] == "c":
        return None
    else:
        handle = parts[0]

    if not handle or handle.startswith("+"):
        return None

    return handle


def now_iso() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def now_filename() -> str:
    """Return a timestamp suitable for file names."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
