"""Command-line interface for tg_discovery."""

from __future__ import annotations

import argparse
import csv
import logging
import os
from typing import List

from .config import load_config
from .google_search import discover_tme_links
from .keywords import bootstrap_keywords
from .scoring import total_score
from .storage import classify_tme_url, save_candidates_to_csv
from .telegram_preview import fetch_telegram_preview
from .utils import extract_handle_from_url, now_filename, now_iso

logger = logging.getLogger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tg_discovery",
        description="Discover Telegram channels via Google CSE and heuristics.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover", help="Discover Telegram channels")
    discover.add_argument("--max-pages", type=int, default=None, help="Pages per query")
    discover.add_argument("--output", type=str, default=None, help="CSV output path")
    discover.add_argument("--min-score", type=int, default=0, help="Minimum score filter")
    discover.add_argument(
        "--query",
        action="append",
        dest="queries",
        help="Override default queries (repeatable)",
    )

    bootstrap = subparsers.add_parser("bootstrap-keywords", help="Suggest new keywords")
    bootstrap.add_argument("--input", type=str, required=True, help="Input CSV path")
    bootstrap.add_argument("--top-n", type=int, default=50, help="Top N tokens")
    bootstrap.add_argument("--output", type=str, default=None, help="Optional output text file")

    return parser


def _run_discover(args: argparse.Namespace) -> int:
    config = load_config()
    queries = args.queries if args.queries else config.default_queries
    max_pages = args.max_pages if args.max_pages is not None else config.max_pages_per_query

    logger.info("Discovering t.me links with %d queries", len(queries))
    discoveries = discover_tme_links(queries, max_pages, config)

    handle_map = {}
    for result in discoveries:
        url = result.get("url", "")
        handle = extract_handle_from_url(url)
        if not handle:
            continue
        if handle not in handle_map:
            handle_map[handle] = result

    rows: List[dict] = []
    discovered_at = now_iso()
    for handle, result in handle_map.items():
        preview = fetch_telegram_preview(handle, config)
        title = preview.get("title", "") if preview else ""
        description = preview.get("description", "") if preview else ""
        score = total_score(handle, title, description)
        if score < args.min_score:
            continue

        original_url = result.get("url", "")
        rows.append(
            {
                "handle": handle,
                "url": f"https://t.me/{handle}",
                "title": title,
                "description": description,
                "google_query": result.get("query", ""),
                "google_title": result.get("google_title", ""),
                "google_snippet": result.get("google_snippet", ""),
                "score": str(score),
                "url_type": classify_tme_url(original_url),
                "discovered_at": discovered_at,
            }
        )

    output_path = args.output or os.path.join("data", f"candidates_{now_filename()}.csv")
    save_candidates_to_csv(output_path, rows)
    logger.info("Saved %d candidates to %s", len(rows), output_path)
    print(output_path)
    return 0


def _run_bootstrap_keywords(args: argparse.Namespace) -> int:
    channels: List[dict] = []
    with open(args.input, "r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            channels.append(
                {
                    "title": row.get("title", "") or "",
                    "description": row.get("description", "") or "",
                }
            )

    suggestions = bootstrap_keywords(channels, top_n=args.top_n)
    lines = [f"{token}\t{count}" for token, count in suggestions]

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
        logger.info("Saved keyword suggestions to %s", args.output)
    else:
        print("\n".join(lines))
    return 0


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "discover":
        return _run_discover(args)
    if args.command == "bootstrap-keywords":
        return _run_bootstrap_keywords(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
