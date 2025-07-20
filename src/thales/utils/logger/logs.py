"""
Logger for Thales project

usage:
    # my_script.py
    from log_config import get_logger

    logger = get_logger(__name__)

    if __name__ == "__main__":
        logger.info("Logging is working")
"""

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)        # create once

LOG_FILE = LOG_DIR / "debug.log"


# Configure logging for development
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5_000, backupCount=5),  # File output
        logging.StreamHandler(),  # Console output
    ],
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("Test")


