from bot.kb_parameters.base import BaseKbParameter, BaseKbParameters
from bot.kb_parameters.classes import (
    BoolKbParameter, CheckBoxKbParameter, NumKbParameter, StrKbParameter
)
from config.config import Config
from config.user import UserConfig


class UserKbParameters(BaseKbParameters):
    def __init__(self, fields_to_validate: list[str]):
        self.parameters: dict[str, BaseKbParameter] = dict(
            temperature=NumKbParameter(min=0, max=2, step=0.1, type=float),
            top_p=NumKbParameter(min=0, max=1, step=0.1, type=float),
            top_k=NumKbParameter(min=1, max=50, step=5, type=int),
            repeat_penalty=NumKbParameter(min=0, max=2, step=0.1, type=float),
            max_tokens=NumKbParameter(min=0, max=4096, step=512, type=int),
            enable_thinking=BoolKbParameter(),
            show_thinking=BoolKbParameter(),
            stream_llm_response=BoolKbParameter(),
            system_prompt=StrKbParameter(),
            answer_with_text=BoolKbParameter(),
            answer_with_voice=BoolKbParameter(),
            # add new parameters here (they should also be in the UserConfig)
            # other_param=NumKbParameter(min=0, max=100, step=10, type=int),
        )
        super().__init__(fields_to_validate)


class VoiceKbParameters(BaseKbParameters):
    def __init__(self, fields_to_validate: list[str]):
        self.parameters: dict[str, BaseKbParameter] = dict(
            voice=CheckBoxKbParameter(
                choices=list(Config.AVAILABLE_VOICES),
                value=list(Config.AVAILABLE_VOICES)[-1],
            ),
        )
        super().__init__(fields_to_validate)


class KbParameters:
    user = UserKbParameters(fields_to_validate=UserConfig.get_dataclass_fields())
    voice = VoiceKbParameters(fields_to_validate=UserConfig.get_dataclass_fields())
