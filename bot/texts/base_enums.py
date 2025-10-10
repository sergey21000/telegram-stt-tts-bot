from enum import Enum


class CallbackEnum(Enum):
    @staticmethod
    def get_callback_name_suffix() -> str:
        return ''

    def get_callback_name(self) -> str:
        return self.name.lower() + self.get_callback_name_suffix()

    @classmethod
    def get_callback_names(cls) -> list[str]:
        return [enum.get_callback_name() for enum in cls]

    @classmethod
    def get_callbacks_dict(cls) -> dict[str, 'CallbackEnum']:
        return {enum.get_callback_name(): enum for enum in cls}


class LangEnumBase(CallbackEnum):
    @staticmethod
    def get_callback_name_suffix() -> str:
        return '_set_lang'
