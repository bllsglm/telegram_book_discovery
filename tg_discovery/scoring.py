"""Heuristic scoring for Telegram channels – Turkish book focused."""

from __future__ import annotations

from typing import Dict, List

from .keywords import (
    CORE_BOOK_KEYWORDS,
    EDU_KEYWORDS,
    FORMAT_KEYWORDS,
    HANDLE_KEYWORDS,
)

# Türkçe dil sinyali
TURKISH_CHARS = "ığüşöçİıĞÜŞÖÇ"
TURKISH_HINT_WORDS = [
    "ve",
    "bir",
    "için",
    "icin",
    "ile",
    "gibi",
    "olan",
    "üzerine",
    "uzerine",
]


def is_probably_turkish(text: str) -> bool:
    """Check if the text is likely Turkish."""
    if not text:
        return False

    t = text.lower()

    # 1) Türkçe karakter varsa güçlü sinyal
    if any(ch in t for ch in TURKISH_CHARS.lower()):
        return True

    # 2) Türkçe kelime tespiti
    hits = sum(1 for w in TURKISH_HINT_WORDS if w in t)
    return hits >= 2


def score_text(title: str, description: str) -> int:
    """Weighted scoring of text based on Turkish book-related keywords."""
    text = f"{title or ''} {description or ''}".lower()
    score = 0

    # Kitap sinyali (en önemli)
    for kw in CORE_BOOK_KEYWORDS:
        if kw in text:
            score += 3

    # Eğitim sinyali
    for kw in EDU_KEYWORDS:
        if kw in text:
            score += 2

    # Format sinyalleri (pdf, epub)
    for kw in FORMAT_KEYWORDS:
        if kw in text:
            score += 1

    return score


def score_handle(handle: str) -> int:
    """Score channel handle based on keyword presence."""
    h = (handle or "").lower()
    score = 0
    for kw in HANDLE_KEYWORDS:
        if kw in h:
            score += 2
    return score


def total_score(handle: str, title: str, description: str) -> int:
    """Calculate final channel score with Turkish detection."""
    combined_text = f"{title or ''} {description or ''}"

    # Eğer Türkçe değilse tamamen ele
    if not is_probably_turkish(combined_text):
        return 0

    base = score_text(title, description) + score_handle(handle)

    return base
