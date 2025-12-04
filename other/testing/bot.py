import os
import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable
from operator import add, sub, not_, gt, lt
from dataclasses import dataclass, asdict
from enum import Enum, StrEnum

from chatgpt_md_converter import telegram_format

from aiogram import Bot, Dispatcher, F, Router, BaseMiddleware
from aiogram.filters import CommandStart, Command, CommandObject, BaseFilter, StateFilter
from aiogram.types import Message, CallbackQuery, BotCommand, InlineKeyboardButton
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram.types import TelegramObject
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

# import nest_asyncio
# nest_asyncio.apply()

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env', override=True)

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

    format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(funcName)s: %(message)s'
    logging.basicConfig(
        level=level,
        format=format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers,
        force=True,
    )

class LoggingConfig:
    TIMEZONE: zoneinfo.ZoneInfo = zoneinfo.ZoneInfo('Europe/Moscow')
    LOG_TO_FILE: bool = False
    LOG_LEVEL: int = logging.INFO


configure_logging(
    log_to_file=LoggingConfig.LOG_TO_FILE,
    level=LoggingConfig.LOG_LEVEL,
    tz=LoggingConfig.TIMEZONE,
)
logger = logging.getLogger(__name__)


BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError('Set the bot token in the BOT_TOKEN variable in the .env file.')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

text = '''<think>
Okay, the user just asked "Как дела?" which translates to "How are you?" in Russian. I need to respond appropriately. Since they're asking about
'''

@dp.message()
async def answer(message: Message):

    await message.answer(text=text)


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info('The bot is launched and ready to work')
        # старт бота
        await dp.start_polling(bot, skip_updates=True)
    # except Exception as ex:
    #     logging.error(f'Error starting the bot: {ex}')
    finally:
        await bot.session.close()
        logging.info('The bot has been stopped')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info('Exiting via Ctrl+C (KeyboardInterrupt)')