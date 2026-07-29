"""Entry point — starts the Telegram bot and wires everything together."""

import logging
from functools import partial

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from bot.config import load_config
from bot.handlers import handle_receipt, handle_start

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main() -> None:
    config = load_config()

    application = ApplicationBuilder().token(config.telegram_bot_token).build()

    receipt_handler = partial(handle_receipt, config=config)
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receipt_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
