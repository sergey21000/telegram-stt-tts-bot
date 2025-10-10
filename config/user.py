from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class BaseConfig:
    def __post_init__(self):
        for key, class_type in self.__annotations__.items():
            self.__dict__[key] = class_type(self.__dict__[key])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def keys(self) -> list[str]:
        return list(self.to_dict().keys())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'BaseConfig':
        return cls(**data)

    @classmethod
    def get_dataclass_fields(cls) -> list[str]:
        return list(cls.__dataclass_fields__.keys())


@dataclass
class UserConfig(BaseConfig):
    temperature: float = 0.2
    top_p: float = 0.95
    top_k: int = 40
    repeat_penalty: float = 1.0
    max_tokens: int = 4096
    enable_thinking: bool = False
    show_thinking: bool = False
    stream_llm_response: bool = False
    system_prompt: str = ''
    user_lang: str = 'ru'
    voice_name: str = 'male_1'
    answer_with_voice: bool = True
    answer_with_text: bool = True

    def get_generation_kwargs(self) -> dict[str, Any]:
        generation_keys = ['temperature', 'top_p', 'top_k', 'repeat_penalty', 'max_tokens']
        generation_kwargs = {k: v for k, v in self.to_dict().items() if k in generation_keys}
        return generation_kwargs
