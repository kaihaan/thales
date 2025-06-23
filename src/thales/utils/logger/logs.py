"""
Logger for Thales project

usage:
    # my_script.py
    from log_config import get_logger

    logger = get_logger(__name__)

    if __name__ == "__main__":
        logger.info("Logging is working")
"""

import logging

# Configure logging for development
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),  # File output
        logging.StreamHandler(),  # Console output
    ],
)

def get_logger(name: str):
    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("Test")


