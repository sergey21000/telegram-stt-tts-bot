from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.database.user_db import DataBase
from bot.kb_parameters.classes import StrKbParameter
from bot.keyboards.keyboards import KbBuilder
from bot.states.states import SettingsState
from bot.texts.languages import Texts
from bot.texts.localization import Localization

from bot.texts.languages import Texts
from bot.kb_parameters.kb_parameters import KbParameters
from bot.keyboards.keyboards import KbBuilder


router: Router = Router()
texts: Texts = Localization.get_texts_by_lang()


@router.callback_query(
    StateFilter(None),
    F.data == texts.MainMenuButtons.user_settings.get_callback_name(),
)
async def user_settings(callback: CallbackQuery, state: FSMContext, db: DataBase, texts: Texts):
    user_id = callback.message.chat.id
    user_config = await db.get_user_config(user_id=user_id)
    await callback.message.answer(
        text=texts.MainMenuButtons.user_settings,
        reply_markup=KbBuilder.kb_from_config(
            kb_parameters=KbParameters.user,
            config=user_config,
            texts=texts,
            btn_texts=texts.UserBtnTexts,
        )
    )
    await state.set_state(SettingsState.user_settings)


@router.callback_query(
    SettingsState.user_settings,
    F.data.in_(KbParameters.user.callbacks),
)
async def change_user_settings(callback: CallbackQuery, state: FSMContext, bot: Bot, db: DataBase, texts: Texts):
    user_id = callback.message.chat.id
    user_config = await db.get_user_config(user_id=user_id)
    kb_parameter = KbParameters.user.callbacks[callback.data]
    curr_value = user_config.to_dict()[kb_parameter.parameter_name]
    if isinstance(kb_parameter, StrKbParameter):
        await callback.message.answer(
            text=texts.KbParameterMessages.wait_input_str_parameter(kb_parameter.parameter_name, curr_value),
        )
        await state.update_data(param_name_to_update=kb_parameter.parameter_name)
        await state.set_state(SettingsState.input_str_param)
        return
    result_status = kb_parameter.get_new_value(curr_value=curr_value, callback_name=callback.data)
    if not result_status.is_ok:
        await bot.answer_callback_query(callback.id, text=texts.KbParameterMessages.out_of_range(
            parameter_name=kb_parameter.parameter_name,
            max=kb_parameter.max,
            min=kb_parameter.min,
        ))
        return
    user_config = await db.update_user_config(user_id=user_id, **result_status.result)
    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=KbBuilder.kb_from_config(
            kb_parameters=KbParameters.user,
            config=user_config,
            texts=texts,
            btn_texts=texts.UserBtnTexts,
        )
    )


@router.message(SettingsState.input_str_param, ~F.text.startswith('/'))
async def set_text_parameter(message: Message, state: FSMContext, db: DataBase, texts: Texts):
    user_id = message.from_user.id
    state_data = await state.get_data()
    param_name_to_update = state_data['param_name_to_update']
    user_config = await db.update_user_config(user_id=user_id, **{param_name_to_update: message.text})
    await message.answer(
        text=texts.MainKbMessages.succes_update_str_parameter(param_name_to_update),
        reply_markup=KbBuilder.main_kb(texts),
    )
    await state.clear()
