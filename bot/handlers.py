"""Telegram handlers: react to incoming receipt photos/documents."""

import logging
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import Config
from ocr.extractor import extract_text
from ocr.parser import parse_receipt
from sheets.client import get_worksheet
from sheets.writer import append_receipt

logger = logging.getLogger(__name__)


async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE, config: Config) -> None:
    """Downloads the incoming photo/document, OCRs it, parses it, and logs it to the sheet."""
    message = update.message
    if message.photo:
        telegram_file = await message.photo[-1].get_file()
    elif message.document:
        telegram_file = await message.document.get_file()
    else:
        await message.reply_text("Please send a receipt as a photo or file.")
        return

    with tempfile.TemporaryDirectory() as tmp_dir:
        image_path = Path(tmp_dir) / "receipt.jpg"
        await telegram_file.download_to_drive(image_path)

        raw_text = extract_text(image_path)
        receipt = parse_receipt(raw_text)

    if receipt.sum is None:
        await message.reply_text("Couldn't read an amount from this receipt. Please try a clearer photo.")
        return

    worksheet = get_worksheet(
        config.google_credentials_path, config.google_sheet_id, config.google_sheet_worksheet
    )
    append_receipt(worksheet, receipt)

    await message.reply_text(
        f"Saved: {receipt.name or 'unknown'} — {receipt.sum} "
        f"({receipt.date.isoformat(sep=' ') if receipt.date else 'no date found'})"
    )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me a photo of a receipt and I'll log it to your Google Sheet."
    )
