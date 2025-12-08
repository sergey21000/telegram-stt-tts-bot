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
    system_prompt: str = 'Старайся отвечать не слишком длинными сообщениями'
    user_lang: str = 'ru'
    voice: str = 'en-US-AvaMultilingualNeural'
    answer_with_voice: bool = True
    answer_with_text: bool = True

    def get_completions_kwargs(self) -> dict[str, Any]:
        completions_kwargs = dict(
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            extra_body=dict(
                top_k=self.top_k,
                repeat_penalty=self.repeat_penalty,
                # reasoning_format='none',
                chat_template_kwargs=dict(
                    enable_thinking=self.enable_thinking,
                ),
            ),
        )
        return completions_kwargs
