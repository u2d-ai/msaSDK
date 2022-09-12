import locale
import os
from functools import lru_cache
from gettext import GNUTranslations
from typing import Dict, Set


class I18N:

    def __init__(self):
        self._locales: Dict[str, Set[GNUTranslations]] = {}
        self._language: str = self.set_language()

    def load_translations(self, translations: Dict[str, GNUTranslations]):
        """Load the GNUTranslations.

        Args:
            translations: the dict with the GNU Translations
        """
        for language, trans in translations.items():
            if language in self._locales:
                self._locales[language].add(trans)
            else:
                self._locales[language] = {trans}

    def set_language(self, language: str = None) -> str:
        """Set the i18n localization language.

        If it is empty, try to read the environment variable `LANGUAGE`/`LANG`, the system default language, in turn.

        Args:
            language: the language to try to set

        Returns:
            the language after the successful setting
        """
        language = language or os.getenv('LANGUAGE') or os.getenv('LANG') or locale.getdefaultlocale()[0]
        self._language = 'zh_CN' if language.lower().startswith('zh') else 'en_US'
        return self._language

    def get_language(self):
        return self._language

    @lru_cache()
    def gettext(self, value: str, language: str = None) -> str:
        """
        This function returns a cached instance of the translated str object.
        Note:
            Caching is used to prevent re-reading the environment every time the translated str object is used.
        """
        language = language or self._language
        if language in self._locales:
            for trans in self._locales[language]:
                # noinspection PyProtectedMember
                if value in trans._catalog:  # type: ignore
                    value = trans.gettext(value)
        return value

    def __call__(self, value, language: str = None) -> str:
        return self.gettext(str(value), language)


i18n = I18N()
