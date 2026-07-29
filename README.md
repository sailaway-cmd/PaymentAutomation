# Telegram Receipt Bot

A Telegram bot that reads a photo of a receipt, extracts the merchant name,
total, and date/time via OCR, and logs it as a new row in a Google Sheet.

## How it works

1. `bot/main.py` starts the bot and registers the handlers in `bot/handlers.py`.
2. When a receipt photo/document arrives, `bot/handlers.py` downloads it and
   calls `ocr/extractor.py`, which runs Tesseract OCR on the image.
3. `ocr/parser.py` parses the raw OCR text into structured fields: name, sum,
   and date/time.
4. `sheets/writer.py` appends those fields as a new row to a Google Sheet,
   using `sheets/client.py` to authenticate and connect via the Google
   Sheets API.
5. `bot/config.py` loads all secrets (bot token, Google credentials path,
   sheet ID) from environment variables via a local `.env` file, which is
   never committed to the repo.

## Setup

### 1. Prerequisites

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and
  available on your `PATH`
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A Google Cloud service account with the Sheets API enabled, and its
  credentials JSON file
- A Google Sheet shared with that service account's email address

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Fill in `.env` with your bot token, path to `credentials.json`, and sheet ID.

### 4. Run the bot

```bash
python -m bot.main
```

Send the bot a photo of a receipt — it will reply with the parsed name, sum,
and date, and append a row to your sheet.

## Running tests

```bash
pytest
```

## Project structure

```
telegram-receipt-bot/
├── bot/          # Telegram entry point, handlers, config
├── ocr/          # OCR text extraction and parsing
├── sheets/       # Google Sheets auth and writing
└── tests/        # Unit tests + sample receipt images
```

## License

MIT — see [LICENSE](LICENSE).
