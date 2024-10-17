import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s - %(module)s',
    )
logger = logging.getLogger(__name__)

import os
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from middlewares import BotMiddleware
from handlers import router


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    raise Exception('Set the bot token to the BOT_TOKEN variable in the .env file')


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

router.message.middleware(BotMiddleware(bot))
dp.include_router(router)


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info('Starting bot...')
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(f'Error starting bot: {ex}')
    finally:
        await bot.session.close()
        logger.info('Bot stopped')


if __name__ == '__main__':
    asyncio.run(main())