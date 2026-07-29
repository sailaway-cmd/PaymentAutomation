"""Runs Tesseract OCR on a receipt image and returns raw text."""

from pathlib import Path

import pytesseract
from PIL import Image


def extract_text(image_path: str | Path) -> str:
    """Runs OCR on the given image file and returns the raw extracted text."""
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)
