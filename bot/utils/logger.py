import sys
import logging
import zoneinfo
from datetime import datetime


def configure_logging(log_to_file: bool, level: int, tz: zoneinfo.ZoneInfo) -> None:
    '''Setting up logging for a specific time zone'''
    logging.Formatter.converter = lambda *args: datetime.now(tz=tz).timetuple()
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_to_file:
        log_file_name = 'bot_log.log'
        handlers.append(logging.FileHandler(log_file_name))

    format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s: %(message)s'
    logging.basicConfig(
        level=level,
        format=format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers,
        force=True,
    )


