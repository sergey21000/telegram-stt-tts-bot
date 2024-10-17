import logging
import asyncio
import re

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

from chatgpt_md_converter import telegram_format

from infer_models import SUPPORT_SYSTEM_ROLE
from infer_utils import (
    convert_ogg_to_wav,
    speech_to_text,
    text_to_text,
    text_to_speech,
)
from config import (
    GENERATION_KWARGS,
    CURR_SPEAKER,
    ALL_SPEAKERS,
    WELCOME_MESSAGE,
    SYSTEM_PROMPT,
)


logger = logging.getLogger(__name__)
router = Router()

if SYSTEM_PROMPT and not SUPPORT_SYSTEM_ROLE:
    logger.warning('System role not supported by this model!')


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(WELCOME_MESSAGE, parse_mode='MarkdownV2')


@router.message(F.text.in_('01234'))
async def change_speaker(message: Message):
    old_speaker_index = int(CURR_SPEAKER['speaker_index'])
    CURR_SPEAKER['speaker_index'] = int(message.text)
    answer = f'Голос был изменен с `{ALL_SPEAKERS[old_speaker_index]}` на `{ALL_SPEAKERS[CURR_SPEAKER["speaker_index"]]}`'
    await message.answer(answer, parse_mode='MarkdownV2')


@router.message(F.voice)
async def from_voice(message: Message, bot: Bot):
    ogg_voice_name = 'voice.ogg'
    wav_voice_name = 'voice.wav'
    await bot.download(message.voice, destination=ogg_voice_name)
    convert_status = convert_ogg_to_wav(ogg_voice_name, wav_voice_name)
    if convert_status == False:
        await message.answer('Произошла ошибка при конвертации ogg в wav ☹')
        return

    recognized_text = await asyncio.to_thread(speech_to_text, wav_voice_name)
    if recognized_text is None:
        await message.answer('Не удалось распознать речь ☹')
        return

    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='typing'):
        generated_text = await asyncio.to_thread(text_to_text, recognized_text, SYSTEM_PROMPT, GENERATION_KWARGS)

    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='record_voice'):
        audio_path_tts = await asyncio.to_thread(text_to_speech, generated_text, CURR_SPEAKER['speaker_index'])

    formatted_text = telegram_format(generated_text)
    audio_file = FSInputFile(audio_path_tts)
    
    await message.answer(formatted_text, parse_mode='HTML')
    await message.answer_voice(audio_file)


@router.message(F.text)
async def from_text(message: Message, bot: Bot):
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='typing'):
        generated_text = await asyncio.to_thread(text_to_text, message.text, SYSTEM_PROMPT, GENERATION_KWARGS)

    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='record_voice'):
        audio_path_tts = await asyncio.to_thread(text_to_speech, generated_text, CURR_SPEAKER['speaker_index'])

    formatted_text = telegram_format(generated_text)
    audio_file = FSInputFile(audio_path_tts)
    
    await message.answer(formatted_text, parse_mode='HTML')
    await message.answer_voice(audio_file)
