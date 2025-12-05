from aiogram import Bot, Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from bot.database.user_db import DataBase
from bot.texts.localization import Localization
from bot.texts.languages import Texts
from bot.types import SpeechToSpeechQueueKwargs
from bot.init.queue import llm_queue


router: Router = Router()
texts: Texts = Localization.get_texts_by_lang()


@router.message(
    StateFilter(None),
    (F.text & ~F.text.startswith('/')) | F.voice,
)
async def put_user_message_to_llm_queue(message: Message, bot: Bot, db: DataBase, texts: Texts):
    user_id = message.from_user.id
    user_config = await db.get_user_config(user_id)
    if not user_config.answer_with_voice and not user_config.answer_with_text:
        await message.answer(texts.ProcessMessages.no_ansewr_mode_selected)
        return

    disable_notification = user_config.answer_with_voice
    bot_answer_message = await message.answer(
        text=texts.ProcessMessages.wait_bot_answer,
        disable_notification=disable_notification,
        parse_mode='HTML',
    )
    llm_worker_kwargs = SpeechToSpeechQueueKwargs(
        user_message=message,
        bot_message=bot_answer_message,
        bot=bot,
        texts=texts,
        user_config=user_config,
    )
    position = await llm_queue.add_task(llm_worker_kwargs.to_dict())
    await bot_answer_message.edit_text(
        text=texts.ProcessMessages.wait_bot_answer_with_position(position=position),
        parse_mode='HTML',
    )
