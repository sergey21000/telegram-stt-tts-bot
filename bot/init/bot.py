import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.init.db import db
from bot.middlewares.db import DbMiddleware
from bot.middlewares.lang import TextsByLangMiddleware
from bot.routers import (
    commands,
    lang,
    speech_to_speech,
    start,
    user_settings,
    voice,
)


logger = logging.getLogger(__name__)


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

db_middleware = DbMiddleware(db)
texts_by_lang_middleware = TextsByLangMiddleware(db)

dp.message.middleware(db_middleware)
dp.callback_query.middleware(db_middleware)
dp.message.middleware(texts_by_lang_middleware)
dp.callback_query.middleware(texts_by_lang_middleware)

dp.include_router(start.router)
dp.include_router(lang.router)
dp.include_router(commands.router)
dp.include_router(user_settings.router)
dp.include_router(voice.router)
dp.include_router(speech_to_speech.router)


async def start_bot(bot: Bot):
    logger.info('The bot has been launched')

async def stop_bot(bot: Bot):
    logger.info('The bot has been stopped')

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)
