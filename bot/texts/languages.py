import importlib
from pathlib import Path

from bot.texts.locales.ru import Texts


locales_path = Path('bot/texts/locales')
LANG_CODES = [
    p.stem
    for p in locales_path.glob('*.py')
    if p.name != '__init__.py'
]
TEXTS_BY_LANG: dict[str, Texts] = {
    code: importlib.import_module(f'bot.texts.locales.{code}').Texts
    for code in LANG_CODES
}
if not TEXTS_BY_LANG:
    raise ValueError("No locale modules found in 'bot/texts/locales'")
