"""Writes parsed receipt data as rows in the Google Sheet."""

from gspread import Worksheet

from ocr.parser import ReceiptData


def append_receipt(worksheet: Worksheet, receipt: ReceiptData) -> None:
    """Appends a new row with the receipt's name, sum, and date/time."""
    date_str = receipt.date.isoformat(sep=" ") if receipt.date else ""
    worksheet.append_row([receipt.name or "", receipt.sum or "", date_str])
