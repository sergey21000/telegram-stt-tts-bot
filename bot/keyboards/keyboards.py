from typing import Type
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.kb_parameters.base import BaseKbParameters
from bot.texts.lang_enum import Langs
from bot.texts.languages import Texts
from bot.texts.base_enums import CallbackEnum
from config.user import UserConfig


class KbBuilder:
    @classmethod
    def build_kb_from_emuns(cls, enums: CallbackEnum):
        builder = InlineKeyboardBuilder()
        for enum in enums:
            cls.add_btn(builder=builder, enum=enum)
        return builder

    @staticmethod
    def add_btn(builder: InlineKeyboardBuilder, enum: CallbackEnum):
        builder.button(
            text=enum.value,
            callback_data=enum.get_callback_name(),
        )

    @classmethod
    def cancel_kb(cls, texts: Texts):
        builder = InlineKeyboardBuilder()
        cls.add_btn(builder=builder, enum=texts.CancelButton.cancel)
        return builder.as_markup()

    @classmethod
    def main_kb(cls, texts: Texts):
        builder = cls.build_kb_from_emuns(enums=texts.MainMenuButtons)
        builder.adjust(2)
        return builder.as_markup()

    @classmethod
    def langs_kb(cls, texts: Texts):
        builder = cls.build_kb_from_emuns(enums=Langs)
        cls.add_btn(builder=builder, enum=texts.BackButton.back_to_main_menu)
        builder.adjust(2)
        return builder.as_markup()

    @classmethod
    def kb_from_config(
        cls,
        kb_parameters: BaseKbParameters,
        config: UserConfig,
        texts: Texts,
        btn_texts: Type,
    ):
        builder = InlineKeyboardBuilder()
        config_dict = config.to_dict()
        for call_name, kb_parameter in kb_parameters.callbacks.items():
            param_name = kb_parameter.parameter_name
            if param_name in config_dict:
                builder.button(
                    text=kb_parameter.get_btn_text(
                        curr_value=config_dict[param_name],
                        callback_name=call_name,
                        btn_texts=btn_texts,
                    ),
                    callback_data=call_name,
                )
        cls.add_btn(builder=builder, enum=texts.BackButton.back_to_main_menu)
        builder.adjust(2)
        return builder.as_markup()
