import asyncio

from dotenv import load_dotenv
load_dotenv()
load_dotenv(dotenv_path='env.llamacpp')

from bot.utils.logging_config import setup_logging
setup_logging()

from loguru import logger


async def main():
    from config.config import Config
    from bot.services.speech import SpeechPipeline

    Config.AVAILABLE_VOICES = await SpeechPipeline.get_available_voices()

    from bot.init.bot import bot, dp
    from bot.init.queue import llm_queue
    from bot.init.db import db
    from bot.init.models import llama_server
    from bot.services.message_handler import MessageHandler
    from bot.texts.locales.ru import Texts
    from bot.texts.localization import Localization

    texts: Texts = Localization.get_texts_by_lang()
    try:
        if llama_server:
            await llama_server.start()
        await db.init()
        await llm_queue.start_workers(worker_func=MessageHandler.speech_to_speech_answer_handler)
        await bot.set_my_commands(commands=texts.BotCommands.commands)
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info('The bot is launched and ready to work')
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        logger.info('The bot has been stopped')
        await llm_queue.stop_workers()


if __name__ == '__main__':
    asyncio.run(main())
