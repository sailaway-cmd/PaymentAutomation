"""Unit tests for the OCR text parsing logic."""

from datetime import datetime

from ocr.parser import parse_receipt


def test_parses_name_sum_and_date():
    raw_text = """SuperMart Grocery
    Date: 24.03.2024 14:32
    Bread            2.50
    Milk             1.80
    TOTAL            4.30
    """

    receipt = parse_receipt(raw_text)

    assert receipt.name == "SuperMart Grocery"
    assert receipt.sum == 4.30
    assert receipt.date == datetime(2024, 3, 24, 14, 32)


def test_missing_fields_return_none():
    receipt = parse_receipt("garbled unreadable text")

    assert receipt.sum is None
    assert receipt.date is None


def test_sum_with_comma_decimal_separator():
    receipt = parse_receipt("Итого: 123,45")

    assert receipt.sum == 123.45
