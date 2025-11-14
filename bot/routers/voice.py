from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from bot.database.user_db import DataBase
from bot.kb_parameters.kb_parameters import KbParameters
from bot.keyboards.keyboards import KbBuilder
from bot.states.states import SettingsState
from bot.texts.languages import Texts
from bot.texts.localization import Localization


router: Router = Router()
texts: Texts = Localization.get_texts_by_lang()


@router.callback_query(
    StateFilter(None),
    F.data == texts.MainMenuButtons.change_voice.get_callback_name(),
)
async def voice_settings(callback: CallbackQuery, state: FSMContext, db: DataBase, texts: Texts):
    await state.set_state(SettingsState.change_voice)
    user_id = callback.message.chat.id
    user_config = await db.get_user_config(user_id=user_id)
    await callback.message.edit_text(
        text=texts.MainKbMessages.change_voice,
        reply_markup=KbBuilder.kb_from_config(
            kb_parameters=KbParameters.voice,
            config=user_config,
            texts=texts,
            btn_texts=texts.UserBtnTexts,
        )
    )


@router.callback_query(
    SettingsState.change_voice,
    F.data.in_(KbParameters.voice.callbacks),
)
async def change_voice_settings(callback: CallbackQuery, db: DataBase, texts: Texts):
    user_id = callback.message.chat.id
    user_config = await db.get_user_config(user_id=user_id)
    kb_parameter = KbParameters.voice.callbacks[callback.data]
    curr_value = user_config.to_dict()[kb_parameter.parameter_name]
    result_status = kb_parameter.get_new_value(curr_value=curr_value, callback_name=callback.data)
    user_config = await db.update_user_config(user_id=user_id, **result_status.result)
    await callback.message.edit_text(
        text=texts.MainKbMessages.change_voice,
        reply_markup=KbBuilder.kb_from_config(
            kb_parameters=KbParameters.voice,
            config=user_config,
            texts=texts,
            btn_texts=texts.UserBtnTexts,
        )
    )
