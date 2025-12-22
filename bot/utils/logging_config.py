import sys
import logging

from loguru import logger

from config.config import Config


def setup_logging() -> None:
    logger.remove()
    logger.add(sys.stderr, level=Config.LOG_LEVEL, colorize=True)
    format = (
        "%(asctime)s.%(msecs)03d | "
        "%(levelname)-8s | "
        "%(module)s:%(funcName)s:%(lineno)d - "
        "%(message)s"
    )
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format=format,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
