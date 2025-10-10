import logging
import zoneinfo


class LoggingConfig:
    TIMEZONE: zoneinfo.ZoneInfo | None = zoneinfo.ZoneInfo('Europe/Moscow')
    LOG_TO_FILE: bool = False
    LOG_LEVEL: int = logging.INFO
