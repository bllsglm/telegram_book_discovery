"""Storage helpers for discovered channels."""

from __future__ import annotations

import csv
import os
from typing import Dict, List
from urllib.parse import urlparse

CANDIDATE_FIELDS = [
    "handle",
    "url",
    "title",
    "description",
    "google_query",
    "google_title",
    "google_snippet",
    "score",
    "url_type",
    "discovered_at",
]


def classify_tme_url(url: str) -> str:
    """Classify a t.me URL as channel/user, message, invite, or unknown."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return "unknown"

    path = parsed.path.strip("/")
    if not path:
        return "unknown"

    if path.startswith("+") or path.startswith("joinchat/"):
        return "invite"

    parts = path.split("/")
    if parts[0] == "s" and len(parts) >= 2:
        if len(parts) >= 3 and parts[2].isdigit():
            return "message"
        return "channel_or_user"

    if len(parts) >= 2 and parts[1].isdigit():
        return "message"

    return "channel_or_user"


def save_candidates_to_csv(path: str, rows: List[Dict[str, str]]) -> None:
    """Save candidate rows to a CSV file."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANDIDATE_FIELDS)
        writer.writeheader()
        for row in rows:
            cleaned = {field: row.get(field, "") for field in CANDIDATE_FIELDS}
            writer.writerow(cleaned)
