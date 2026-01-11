# tg_discovery

Discover Telegram channels that likely share document-like content by querying Google Programmable Search (Custom Search API), scraping the public Telegram preview, and applying simple keyword scoring.

## Prerequisites
- Python 3.10+
- Google Programmable Search Engine configured to focus on `t.me`
- Google Custom Search API key and CSE CX

## Setup
1. Create a `.env` file based on `.env.example`.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Run discovery with default queries:

```bash
python -m tg_discovery discover
```

Optional flags:
- `--max-pages` to override pages per query
- `--output` to set CSV path
- `--min-score` to filter low scores
- `--query` to override default queries (repeatable)

Bootstrap keyword suggestions from a discovery CSV:

```bash
python -m tg_discovery bootstrap-keywords --input data/candidates_YYYYMMDDTHHMMSSZ.csv
```

## Notes
- Results are saved under `data/` by default.
- The tool only uses public preview pages and does not call the Telegram API.
# telegram_book_discovery
