from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command, CommandObject
from bot.database.user_db import DataBase
from bot.filters.filters import Filters
from bot.kb_parameters.kb_parameters import KbParameters
from bot.keyboards.keyboards import KbBuilder
from bot.texts.localization import Localization
from bot.texts.languages import Texts
from aiogram.enums import ParseMode

from bot.states.states import SettingsState
from bot.utils.commands import CommandParser
from config.config import Config
from config.user import UserConfig


router: Router = Router()
texts: Texts = Localization.get_texts_by_lang()


@router.message(Command('help'))
async def settings(message: Message, state: FSMContext, texts: Texts):
    await message.answer(
        text=texts.MainKbMessages.get_help_info(commands_info=texts.BotCommands.commands_info),
        reply_markup=KbBuilder.main_kb(texts),
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == texts.MainMenuButtons.help.get_callback_name())
async def bot_info(callback: CallbackQuery, texts: Texts):
    await callback.message.edit_text(
        text=texts.MainKbMessages.get_help_info(commands_info=texts.BotCommands.commands_info),
        reply_markup=KbBuilder.main_kb(texts),
        parse_mode=ParseMode.HTML,
    )

@router.message(Command('settings'))
async def settings(message: Message, state: FSMContext, db: DataBase, texts: Texts):
    user_id = message.from_user.id
    user_config = await db.get_user_config(user_id=user_id)
    await message.answer(
        text=texts.MainMenuButtons.user_settings,
        reply_markup=KbBuilder.kb_from_config(
            kb_parameters=KbParameters.user,
            config=user_config,
            btn_texts=texts.UserBtnTexts,
        )
    )
    await state.set_state(SettingsState.user_settings)


@router.message(Command('getparams'))
async def set_param_from_command(message: Message, db: DataBase, texts: Texts):
    user_id = message.from_user.id
    user_config = await db.get_user_config(user_id=user_id)
    info = texts.KbParameterMessages.getparams_message
    for key, value in user_config.to_dict().items():
        info += f'{key}: {value}\n'
    await message.answer(info)


@router.callback_query(F.data == texts.MainMenuButtons.get_params.get_callback_name())
async def get_params(callback: CallbackQuery, db: DataBase, texts: Texts):
    user_id = callback.message.chat.id
    user_config = await db.get_user_config(user_id=user_id)
    info = texts.KbParameterMessages.getparams_message
    for key, value in user_config.to_dict().items():
        info += f'{key}: {value}\n'
    await callback.message.answer(info)


@router.message(Command('resetparams'))
async def set_param_from_command(message: Message, db: DataBase, texts: Texts):
    user_id = message.from_user.id
    user_config = await db.get_user_config(user_id=user_id)
    await db.save_user_config(user_id=user_id, config=UserConfig(user_lang=user_config.user_lang))
    await message.answer(
        text=texts.KbParameterMessages.success_resetparams,
        reply_markup=KbBuilder.main_kb(texts),
    )


@router.message(Command('getid'), Filters.admin_filter)
async def get_chat_id(message: Message, bot: Bot):
    info = f'<b>Current Chat ID:</b> {message.chat.id}'
    await bot.send_message(chat_id=Config.ADMIN_CHAT_ID, text=info, parse_mode=ParseMode.HTML)
    if message.chat.type in ('group', 'supergroup'):
        await message.delete()


@router.message(Command(commands=['set', 'reset']))
async def update_parameter_from_command(message: Message, command: CommandObject, db: DataBase, bot: Bot, texts: Texts):
    user_id = message.from_user.id
    if command.command == 'reset':
        parameter_dict = await CommandParser.parse_reset_parameter_handle(
            command=command, message=message, texts=texts,
        )
        if not parameter_dict:
            return
        user_config = await db.get_user_config(user_id=user_id)
        default_config = UserConfig()
        parameter_dict['parameter_value'] = default_config.to_dict()[parameter_dict['parameter_name']]
    elif command.command == 'set':
        parameter_dict = await CommandParser.parse_set_parameter_handle(
            command=command, message=message, texts=texts,
        )
        if not parameter_dict:
            return
    user_config = await db.update_user_config(
        user_id=user_id,
        **{parameter_dict['parameter_name']: parameter_dict['parameter_value']},
    )
    updated_value = user_config.to_dict()[parameter_dict['parameter_name']]
    await message.answer(
        text=texts.KbParameterMessages.success_update_parameter(
        updated_name=parameter_dict['parameter_name'],
        updated_value=updated_value,
    ))

