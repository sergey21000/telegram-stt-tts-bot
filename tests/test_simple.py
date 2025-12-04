import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message

from dotenv import load_dotenv
load_dotenv()

# from bot.init.bot import bot, dp
# from bot.init.queue import llm_queue
# from bot.init.db import db
# from bot.services.executor_handlers import speech_to_speech_answer_handler
# from bot.texts.locales.ru import Texts
# from bot.texts.localization import Localization

from bot.utils.logger import configure_logging
from config.logger import LoggingConfig
from config.config import Config

configure_logging(
    log_to_file=LoggingConfig.LOG_TO_FILE,
    level=LoggingConfig.LOG_LEVEL,
    tz=LoggingConfig.TIMEZONE,
)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
test_router = Router()

# dp.include_router(speech_to_speech.router)

# llm_worker_kwargs = dict(
    # user_message=message,
    # bot_message=bot_answer_message,
    # bot=bot,
    # texts=texts,
    # user_config=user_config,
# )


async def send_test_message():
    info = 'Пришлите любой запрос для начала тестирования бота'
    bot_message = await bot.send_message(
        Config.ADMIN_CHAT_ID,
        text=info,
        parse_mode=ParseMode.HTML,
    )
    return bot_message
    
@test_router.message()
async def test(message: Message, bot: Bot):
    await asyncio.sleep(3)
    await dp.stop_polling()

dp.include_router(test_router)



async def main():
    try:
        # await db.init()
        # await llm_queue.start_workers(worker_func=speech_to_speech_answer_handler, warmup_pool=True)
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info('The bot is launched and ready to work')
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        logging.info('The bot has been stopped')
        # await llm_queue.stop_workers()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info('Exiting via Ctrl+C (KeyboardInterrupt)')