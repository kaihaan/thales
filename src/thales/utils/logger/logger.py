"""
Logger for Thales project

usage:
- logger.debug("output here")
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

logger = logging.getLogger(__name__)

if __name__ == "main":
    logger.debug("Test")


