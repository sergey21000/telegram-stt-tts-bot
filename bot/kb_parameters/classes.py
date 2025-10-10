from dataclasses import dataclass
from typing import Any, Type

from bot.kb_parameters.base import BaseKbParameter


@dataclass
class SetParamStatus:
    is_ok: bool
    result: dict[str, Any]


@dataclass
class NumKbParameter(BaseKbParameter):
    min: int | float | None = None
    max: int | float | None = None
    step: int | float | None = None
    type: Type = float

    def __post_init__(self):
        self.increase_subtype = 'increase'
        self.decrease_subtype = 'decrease'

    def copy_with_subtype(self, subtype: str) -> 'NumKbParameter':
        init_kwargs = {**self.to_dict(), 'subtype': subtype}
        return type(self)(**init_kwargs)

    def get_callback_dict(self) -> dict[str, BaseKbParameter]:
        increase_obj = self.copy_with_subtype(subtype=self.increase_subtype)
        decrease_obj = self.copy_with_subtype(subtype=self.decrease_subtype)
        return {
            decrease_obj.get_callback_name(): decrease_obj,
            increase_obj.get_callback_name(): increase_obj,
        }

    def get_btn_text(self, curr_value: float, callback_name: str, btn_texts: Type) -> str:
        if self.subtype == self.increase_subtype:
            symbol = '🔼'
            subsymbol = '➕'
        elif self.subtype == self.decrease_subtype:
            symbol = '🔽'
            subsymbol = '➖'
        else:
            symbol = ''
        btn_text = getattr(btn_texts, self.parameter_name, '') or self.parameter_name
        return f'{symbol} {btn_text}: {curr_value}{subsymbol}{self.step}'

    def validate_new_value(self, new_value: float | int | bool) -> bool:
        return self.min <= self.type(new_value) <= self.max

    def get_new_value(self, curr_value: float, callback_name: str) -> SetParamStatus:
        if self.subtype == self.increase_subtype:
            new_value = curr_value + self.step
        elif self.subtype == self.decrease_subtype:
            new_value = curr_value - self.step
        if not self.min <= new_value <= self.max:
            result = {self.parameter_name: self.type(curr_value)}
            return SetParamStatus(is_ok=False, result=result)
        result = {self.parameter_name: self.type(round(new_value, 1))}
        return SetParamStatus(is_ok=True, result=result)


@dataclass
class BoolKbParameter(BaseKbParameter):
    type: Type = bool

    def __post_init__(self):
        self.suffix = self.suffix or '_bool'

    def get_btn_text(self, curr_value: bool, btn_texts: Type, *args, **kwargs) -> str:
        symbol = 'ON ✅' if curr_value else 'OFF ❌'
        btn_text = getattr(btn_texts, self.parameter_name, '') or self.parameter_name
        return f'{symbol}: {btn_text}'

    def validate_new_value(self, new_value: bool) -> bool:
        return isinstance(new_value, bool)

    def get_new_value(self, curr_value: bool, *args, **kwargs) -> SetParamStatus:
        new_value_dict = {self.parameter_name: self.type(not curr_value)}
        return SetParamStatus(is_ok=True, result=new_value_dict)


@dataclass
class CheckBoxKbParameter(BaseKbParameter):
    choices: list[str]
    value: str
    type: Type = str

    def __post_init__(self):
        self.suffix = self.suffix or '_checkbox'
        self.subtype = self.value

    def copy_with_value(self, value: str) -> 'CheckBoxKbParameter':
        init_kwargs = {**self.to_dict(), 'value': value}
        return type(self)(**init_kwargs)

    def get_callback_dict(self) -> dict[str, BaseKbParameter]:
        callback_dict = dict()
        for choice in self.choices:
            obj = self.copy_with_value(value=choice)
            callback_dict.update({obj.get_callback_name(): obj})
        return callback_dict

    def get_btn_text(self, curr_value: str, btn_texts: Type, *args, **kwargs) -> str:
        symbol = f'{self.value} ✅' if self.value == curr_value else f'{self.value} ❌'
        btn_text = getattr(btn_texts, self.parameter_name, '') or self.parameter_name
        return f'{symbol}: {btn_text}'

    def get_new_value(self, curr_value: str, *args, **kwargs) -> SetParamStatus:
        new_value_dict = {self.parameter_name: self.type(self.value)}
        return SetParamStatus(is_ok=True, result=new_value_dict)


@dataclass
class StrKbParameter(BaseKbParameter):
    type: Type = str

    def __post_init__(self):
        self.suffix = self.suffix or '_str'

    def get_btn_text(self, curr_value: str, btn_texts: Type, *args, **kwargs):
        btn_text = getattr(btn_texts, self.parameter_name, '') or self.parameter_name
        return f'✍ {btn_text}'
