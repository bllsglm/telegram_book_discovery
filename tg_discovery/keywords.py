"""Keyword lists and bootstrap helper for Turkish book discovery."""

from __future__ import annotations

import re
from collections import Counter
from typing import Dict, Iterable, List, Tuple

# -------------------------------------------------------------------
# 1) TÜRKÇE KİTAP / EDEBİYAT / KÜLTÜR KELİMELERİ
# -------------------------------------------------------------------

CORE_BOOK_KEYWORDS: List[str] = [
    # Genel "kitap" varyasyonları
    "kitap",
    "kitaplar",
    "kitaplik",
    "kitaplık",

    # Edebiyat / roman / hikâye / öykü
    "roman",
    "romanlar",
    "edebiyat",
    "hikaye",
    "hikâye",
    "oyku",
    "öykü",

    # Okuma kültürü
    "okuma",
    "okuma kulübü",
    "okuma grubu",

    # Kütüphane
    "kutuphane",
    "kütüphane",
    "kutuphanesi",
    "kütüphanesi",

    # Arşiv
    "arsiv",
    "arşiv",
    "arsivi",
    "arşivi",

    # E-kitap varyantları
    "ekitap",
    "e-kitap",
    "e kitap",
]

# -------------------------------------------------------------------
# 2) FORMAT SİNYALLERİ (ikincil öneme sahip)
# -------------------------------------------------------------------

FORMAT_KEYWORDS: List[str] = [
    "pdf",
    "epub",
    "mobi",
    "dokuman",
    "doküman",
    "not",
    "notlar",
    "slayt",
]

# -------------------------------------------------------------------
# 3) TÜRKÇE EĞİTİM MATERYALLERİ (KPSS / YKS vb.)
# -------------------------------------------------------------------

EDU_KEYWORDS: List[str] = [
    "ders",
    "ders notu",
    "konu anlatımı",
    "konu anlatimli",
    "cikmis soru",
    "çıkmış soru",
    "cikmis sorular",
    "çıkmış sorular",
    "deneme",

    # Sınavlar
    "yks",
    "tyt",
    "ayt",
    "kpss",
    "ales",
    "dgs",
    "yokdil",
    "yökdil",
    "yok dil",
    "yök dil",
]

# -------------------------------------------------------------------
# 4) HANDLE İÇİN ANAHTAR KELİMELER
# -------------------------------------------------------------------

HANDLE_KEYWORDS: List[str] = [
    "kitap",
    "kitaplik",
    "kitaplık",
    "roman",
    "edebiyat",
    "okuma",
    "ekitap",
    "kütüphane",
    "kutuphane",
    "arsiv",
    "arşiv",
    "arsivi",
    "arşivi",
    "depo",
    "deposu",

    # Eğitim
    "yks",
    "kpss",
    "ales",
    "dgs",
]

# -------------------------------------------------------------------
# 5) STOPWORDS (bootstrap temizliği için)
# -------------------------------------------------------------------

STOPWORDS = {
    # English
    "the", "and", "or", "a", "an", "of", "to", "in", "for", "with", "is", "are",
    "this", "that", "on", "by", "from", "at", "as", "be", "it", "we", "you",
    "your", "our", "will", "file",

    # Turkish
    "ve", "bir", "bu", "da", "de", "ile", "icin", "için", "gibi", "daha",
    "olan", "uzerine", "üzerine",
}

# -------------------------------------------------------------------
# 6) KEYWORD GROUPING
# -------------------------------------------------------------------

def get_keyword_lists() -> Dict[str, List[str]]:
    """Return keyword lists grouped by category."""
    return {
        "core": CORE_BOOK_KEYWORDS,    # kitap / roman / edebiyat
        "format": FORMAT_KEYWORDS,     # pdf / epub / mobi
        "edu": EDU_KEYWORDS,           # ders / çıkmış soru / sınavlar
    }

# -------------------------------------------------------------------
# 7) BOOTSTRAP — otomatik yeni keyword keşfi
# -------------------------------------------------------------------

def bootstrap_keywords(channels: List[dict], top_n: int = 50) -> List[Tuple[str, int]]:
    """
    Extract frequent tokens from channel metadata for keyword expansion.
    Used for improving future keyword lists based on real discovered data.
    """
    counter: Counter[str] = Counter()

    for channel in channels:
        title = channel.get("title", "") or ""
        description = channel.get("description", "") or ""
        text = f"{title} {description}".lower()

        # Tokenize (latin-only)
        tokens = re.findall(r"[a-z0-9çğıöşüİÇĞİÖŞÜ]+", text)

        for token in tokens:
            if len(token) < 3:
                continue
            if token in STOPWORDS:
                continue
            if token.isdigit():
                continue

            counter[token] += 1

    return counter.most_common(top_n)
