import os
import sys
from loguru import logger

from config.config import Config


def setup_logging() -> None:
    logger.remove()
    logger.add(sys.stderr, level=Config.LOG_LEVEL, colorize=True)
