from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any, Type


@dataclass(kw_only=True)
class BaseKbParameter(ABC):
    parameter_name: str = ''
    is_active: bool = True
    suffix: str = ''
    subtype: str = ''

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def get_callback_name_suffix(self, suffix: str = '', *args, **kwargs) -> str:
        suffix = suffix or self.suffix
        subtype_suffix = f'_{self.subtype}' if self.subtype else ''
        return subtype_suffix + suffix

    def get_callback_name(self, ) -> str:
        return self.parameter_name + self.get_callback_name_suffix()

    def get_callback_dict(self) -> dict[str, 'BaseKbParameter']:
        return {self.get_callback_name(): self}

    @abstractmethod
    def get_btn_text(self, curr_value: Any, btn_texts: Type, *args, **kwargs) -> str: ...


class BaseKbParameters:
    def __init__(self, fields_to_validate: list[str] | None = None):
        if not hasattr(self, 'parameters') or not isinstance(self.parameters, dict):
            raise AttributeError('The child class is missing the self.parameters dictionary')
        for key, param in self.parameters.items():
            if not param.parameter_name:
                param.parameter_name = key
        self.callbacks = self.get_callbacks_dict(self.parameters)
        if fields_to_validate:
            self.validate_fields(target_fields=fields_to_validate)

    @classmethod
    def get_callbacks_dict(cls, params_dict: dict[str, BaseKbParameter]) -> dict[str, BaseKbParameter]:
        callbacks_dict = dict()
        for key, parameter in params_dict.items():
            if parameter.is_active:
                callbacks_dict.update(parameter.get_callback_dict())
        return callbacks_dict

    def validate_fields(self, target_fields: list[str]) -> None:
        missing_fields = [key for key in self.parameters if key not in target_fields]
        if missing_fields:
            raise ValueError(
                f'In the class "{self.__class__.__name__}" there are extra fields: {missing_fields} \n'
                f'Available fields: {list(self.parameters.keys())}\n'
                f'Allowed fields: {target_fields}'
            )
