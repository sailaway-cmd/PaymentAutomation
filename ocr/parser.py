"""Parses raw OCR text from a receipt into structured fields."""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

_SUM_PATTERN = re.compile(
    r"(?:total|sum|amount|итого|сумма)\D{0,30}(\d[\d\s]*[.,]\d{2})",
    re.IGNORECASE,
)
_FALLBACK_SUM_PATTERN = re.compile(r"(\d[\d\s]*[.,]\d{2})")

_DATE_PATTERNS = [
    (re.compile(r"(\d{2})[./-](\d{2})[./-](\d{4})(?:\D+(\d{2}):(\d{2}))?"), "%d.%m.%Y %H:%M"),
    (re.compile(r"(\d{4})[./-](\d{2})[./-](\d{2})(?:\D+(\d{2}):(\d{2}))?"), "%Y.%m.%d %H:%M"),
]


@dataclass
class ReceiptData:
    name: Optional[str]
    sum: Optional[float]
    date: Optional[datetime]


def _find_sum(text: str) -> Optional[float]:
    match = _SUM_PATTERN.search(text) or _FALLBACK_SUM_PATTERN.search(text)
    if not match:
        return None
    raw = match.group(1).replace(" ", "").replace(",", ".")
    try:
        return float(raw)
    except ValueError:
        return None


def _find_date(text: str) -> Optional[datetime]:
    for pattern, _ in _DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        groups = match.groups()
        try:
            if len(groups[0]) == 4:  # year-first pattern
                year, month, day, hour, minute = groups
            else:
                day, month, year, hour, minute = groups
            hour = hour or "00"
            minute = minute or "00"
            return datetime(int(year), int(month), int(day), int(hour), int(minute))
        except ValueError:
            continue
    return None


def _find_name(text: str) -> Optional[str]:
    for line in text.splitlines():
        stripped = line.strip()
        if len(stripped) >= 3 and any(char.isalpha() for char in stripped):
            return stripped
    return None


def parse_receipt(raw_text: str) -> ReceiptData:
    """Extracts name, sum, and date/time from raw OCR text."""
    return ReceiptData(
        name=_find_name(raw_text),
        sum=_find_sum(raw_text),
        date=_find_date(raw_text),
    )
