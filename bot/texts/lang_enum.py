from enum import Enum

from bot.texts.base_enums import LangEnumBase
from bot.texts.languages import LANG_CODES


Langs = Enum(
    value='Langs',
    names={code: code for code in LANG_CODES},
    type=LangEnumBase,
)
