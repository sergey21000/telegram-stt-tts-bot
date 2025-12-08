from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.keyboards import KbBuilder
from bot.texts.localization import Localization
from bot.texts.languages import Texts


router: Router = Router()
texts: Texts = Localization.get_texts_by_lang()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, texts: Texts):
    await state.clear()
    await message.answer(
        text=texts.MainKbMessages.main_menu,
        reply_markup=KbBuilder.main_kb(texts),
        parse_mode='HTML',
    )


@router.callback_query(F.data == texts.BackButton.back_to_main_menu.get_callback_name())
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext, texts: Texts):
    await state.clear()
    await callback.message.edit_text(
        text=texts.MainKbMessages.main_menu,
        reply_markup=KbBuilder.main_kb(texts),
    )
