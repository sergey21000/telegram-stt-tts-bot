from bot.texts.languages import TEXTS_BY_LANG, Texts
from config.config import Config


class Localization:
    @staticmethod
    def get_texts_by_lang(lang: str | None = None) -> Texts:
        if not lang:
            lang = Config.DEFAULT_USER_LANG
        texts = TEXTS_BY_LANG.get(lang)
        return texts
