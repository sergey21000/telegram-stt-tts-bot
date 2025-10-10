from aiogram.types import Message
from aiogram.filters import CommandObject
from aiogram.enums import ParseMode

from bot.kb_parameters.classes import BoolKbParameter
from bot.texts.languages import Texts
from bot.kb_parameters.kb_parameters import KbParameters


class CommandParser:
    @staticmethod
    def check_str_is_number(str_number: str) -> bool:
        try:
            float(str_number)
            return True
        except ValueError:
            return False

    @classmethod
    async def parse_reset_parameter_handle(
        cls,
        command: CommandObject,
        message: Message,
        texts: Texts,
    ) -> dict[str, str | float] | None:
        parameter_name = command.args.strip()
        if not parameter_name:
            await message.answer(text=texts.KbParameterMessages.invalid_parameter_message(), parse_mode=ParseMode.HTML)
            return
        if len(parameter_name.split()) != 1:
            await message.answer(text=texts.KbParameterMessages.invalid_parameter_message(), parse_mode=ParseMode.HTML)
            return
        kb_parameter = KbParameters.user.parameters.get(parameter_name)
        if not kb_parameter:
            await message.answer(text=texts.KbParameterMessages.parameter_is_missing(
                parameter_name=parameter_name,
            ))
            return
        return dict(parameter_name=parameter_name)

    @classmethod
    async def parse_set_parameter_handle(
        cls,
        command: CommandObject,
        message: Message,
        texts: Texts,
    ) -> dict[str, str | float] | None:        
        if not command.args.strip():
            await message.answer(text=texts.KbParameterMessages.invalid_parameter_message(), parse_mode=ParseMode.HTML)
            return
        parameter_name_and_value = command.args.strip().split()
        if len(parameter_name_and_value) != 2:
            await message.answer(text=texts.KbParameterMessages.invalid_parameter_message(), parse_mode=ParseMode.HTML)
            return
        parameter_name, parameter_value = parameter_name_and_value
        if not cls.check_str_is_number(parameter_value):
            await message.answer(text=texts.KbParameterMessages.str_not_is_number())
            return
        kb_parameter = KbParameters.user.parameters.get(parameter_name)
        if not kb_parameter:
            await message.answer(text=texts.KbParameterMessages.parameter_is_missing(
                parameter_name=parameter_name,
            ))
            return
        if isinstance(kb_parameter, BoolKbParameter):
            parameter_value = int(parameter_value)
        parameter_value = kb_parameter.type(parameter_value)
        if not kb_parameter.validate_new_value(parameter_value):
            await message.answer(text=texts.KbParameterMessages.out_of_range(
                parameter_name=parameter_name,
                max=kb_parameter.max,
                min=kb_parameter.min,
            ))
            return
        return dict(parameter_name=parameter_name, parameter_value=parameter_value)
