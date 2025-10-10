from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from bot.database.user_db import DataBase
from bot.keyboards.keyboards import KbBuilder
from bot.states.states import SettingsState
from bot.texts.lang_enum import Langs
from bot.texts.languages import Texts
from bot.texts.localization import Localization


router: Router = Router()
texts: Texts = Localization.get_texts_by_lang()


@router.callback_query(
    StateFilter(None),
    F.data == texts.MainMenuButtons.change_lang.get_callback_name(),
)
async def lang_settings(callback: CallbackQuery, state: FSMContext, texts: Texts):
    await state.set_state(SettingsState.change_lang)
    await callback.message.edit_text(
        text=texts.MainKbMessages.change_lang,
        reply_markup=KbBuilder.langs_kb(texts),
    )


@router.callback_query(SettingsState.change_lang, F.data.in_(Langs.get_callback_names()))
async def change_lang_settings(callback: CallbackQuery, db: DataBase, texts: Texts):
    user_id = callback.message.chat.id
    new_lang = Langs.get_callbacks_dict()[callback.data]
    user_config = await db.update_user_config(user_id=user_id, user_lang=new_lang.value)
    texts = Localization.get_texts_by_lang(lang=new_lang.value)
    await callback.message.edit_text(
        text=texts.MainKbMessages.change_lang,
        reply_markup=KbBuilder.langs_kb(texts),
    )
