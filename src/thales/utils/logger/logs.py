"""
Logger for Thales project

usage:
    # my_script.py
    from thales.utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Logging is working")
    logger.debug("Debug trace msg...")
"""

import logging
from logging import Logger

# Configure logging for development
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),  # File output
        logging.StreamHandler(),  # Console output
    ],
)

def get_logger(name: str) -> Logger:
    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("Test")


