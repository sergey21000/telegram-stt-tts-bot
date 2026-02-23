import sys
import logging

from loguru import logger

from config.config import Config


# filter for isolation default autoinit loguru handler 
# so as not to delete the default handler (logger.remove()) 
# and so that it logs unnecessarily
class IsolationDefaultHandlerFilter:
    """
    A filter for isolating the default logging handler (which is initialized automatically)
    to avoid having to call logger.remove() (as is commonly done and recommended in the 
    documentation) while preventing the default handler from writing unnecessary log entries.

    Args:
        logger_extras: A list of extra values for loggers that should 
                       not be logged by the default auto-initialized handler
    """
    def __init__(self, logger_extras: list[str]):
        self.logger_extras = logger_extras

    def __call__(self, record):
        for logger_extra in self.logger_extras:
            if logger_extra in record['extra']:
                return False
        return True


# set log level for chatbot app
if Config.CHATBOT_LOG_LEVEL:
    if 0 in logger._core.handlers:
        if hasattr(logger._core.handlers[0]._filter, 'logger_extras'):
            logger._core.handlers[0]._filter.logger_extras.append('stt_tts_chatbot')
        else:
            logger._core.handlers[0]._filter = IsolationDefaultHandlerFilter(
                logger_extras=['stt_tts_chatbot']
            )
    logger.add(
        sys.stderr,
        level=Config.CHATBOT_LOG_LEVEL,
        filter=lambda record: 'stt_tts_chatbot' in record['extra'],
        colorize=True,
    )
    logger = logger.bind(stt_tts_chatbot=True)
    # print('logger._core.handlers from bot', logger._core.handlers)


# set log level for logging (for example, aiogram)
def setup_logging(level: int | str = logging.INFO) -> None:
    """Настройка корневого логгера, если он еще не настроен"""
    LOG_FORMAT = (
        '%(asctime)s.%(msecs)03d | '
        '%(levelname)-8s | '
        '%(name)s:%(funcName)s:%(lineno)d - '
        '%(message)s'
    )
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
        ))
        root.addHandler(handler)
    else:
        for handler in root.handlers:
            handler.setFormatter(logging.Formatter(
                fmt=LOG_FORMAT,
                datefmt=DATE_FORMAT,
            ))
    root.setLevel(level)
    # root.propagate = False


if Config.LOGGING_LOG_LEVEL:
    setup_logging(level=Config.LOGGING_LOG_LEVEL)
