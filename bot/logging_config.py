from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_dir: str = "logs", filename: str = "trading_bot.log") -> Path:
    """Configure application logging and return the log file path."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    full_path = log_path / filename

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers when script is run repeatedly in the same session.
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(full_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return full_path
