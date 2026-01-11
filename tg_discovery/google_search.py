"""Google Custom Search API integration."""

from __future__ import annotations

import logging
import time
from typing import Dict, List

import requests

from .config import Config

logger = logging.getLogger(__name__)


def search_google_cse(query: str, start: int, config: Config) -> Dict:
    """Call Google Custom Search API and return the JSON payload."""
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": config.google_api_key,
        "cx": config.google_cse_cx,
        "q": query,
        "num": 10,
        "start": start,
    }
    response = requests.get(endpoint, params=params, timeout=config.request_timeout)
    response.raise_for_status()
    return response.json()


def discover_tme_links(queries: List[str], max_pages: int, config: Config) -> List[Dict[str, str]]:
    """Discover t.me links using Google CSE across multiple queries and pages."""
    results: List[Dict[str, str]] = []
    for query in queries:
        for page in range(max_pages):
            start = 1 + page * 10
            try:
                payload = search_google_cse(query, start, config)
            except requests.RequestException as exc:
                logger.warning("Google CSE error for query '%s': %s", query, exc)
                time.sleep(1.0)
                continue

            for item in payload.get("items", []):
                link = item.get("link", "")
                if "t.me/" not in link:
                    continue
                results.append(
                    {
                        "query": query,
                        "google_title": item.get("title", ""),
                        "google_snippet": item.get("snippet", ""),
                        "url": link,
                    }
                )

            time.sleep(1.0)

    return results
