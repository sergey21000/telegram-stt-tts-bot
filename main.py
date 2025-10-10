import logging
import asyncio

from dotenv import load_dotenv
load_dotenv()

from bot.utils.logger import configure_logging
from config.logger import LoggingConfig

configure_logging(
    log_to_file=LoggingConfig.LOG_TO_FILE,
    level=LoggingConfig.LOG_LEVEL,
    tz=LoggingConfig.TIMEZONE,
)

from bot.init.bot import bot, dp
from bot.init.queue import llm_queue
from bot.init.db import db
from bot.services.executor_handlers import speech_to_speech_answer_handler
from bot.texts.locales.ru import Texts
from bot.texts.localization import Localization


logger = logging.getLogger(__name__)
texts: Texts = Localization.get_texts_by_lang()


async def main():
    try:
        await db.init()
        await llm_queue.start_workers(worker_func=speech_to_speech_answer_handler, warmup_pool=True)
        await bot.set_my_commands(commands=texts.BotCommands.commands)
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info('The bot is launched and ready to work')
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        logging.info('The bot has been stopped')
        await llm_queue.stop_workers()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info('Exiting via Ctrl+C (KeyboardInterrupt)')
