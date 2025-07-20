"""
Logger for Thales project

usage:
    # my_script.py
    from thales.utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Logging is working")
    logger.debug("Debug trace msg...")
"""

from pathlib import Path
from logging.handlers import RotatingFileHandler
import logging

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


