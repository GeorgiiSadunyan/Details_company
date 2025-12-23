"""
Базовый класс для детали (запчасти).
Содержит общие поля и валидацию для всех версий Detail.
"""

import re
from abc import ABC


class DetailBase(ABC):
    """
    Базовый абстрактный класс для детали.

    Attributes:
        article (str): Артикул детали (уникальный идентификатор)
        name (str): Наименование детали
    """

    def __init__(self, article: str, name: str):
        self.article = article
        self.name = name

    # ==================== ARTICLE ====================

    @property
    def article(self) -> str:
        """Артикул детали"""
        return self._article

    @article.setter
    def article(self, value: str):
        if not self._validate_article(value):
            raise ValueError(
                f"Некорректный артикул детали: '{value}'. "
                "Артикул должен содержать от 1 до 50 символов (буквы, цифры, дефисы)."
            )
        self._article = value

    @staticmethod
    def _validate_article(value) -> bool:
        """
        Валидация артикула.

        Правила:
        - Строка от 1 до 50 символов
        - Может содержать: латинские буквы, цифры, дефисы
        - Примеры: "FLT-001", "BRK-045", "OIL5W40"

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        if not isinstance(value, str):
            return False

        # Артикул: буквы (A-Z, a-z), цифры, дефисы
        pattern = r"^[A-Za-z0-9\-]+$"
        return 1 <= len(value) <= 50 and bool(re.match(pattern, value))

    # ==================== NAME ====================

    @property
    def name(self) -> str:
        """Наименование детали"""
        return self._name

    @name.setter
    def name(self, value: str):
        if not self._validate_name(value):
            raise ValueError(
                f"Некорректное наименование детали: '{value}'. "
                "Название должно содержать от 1 до 100 символов."
            )
        self._name = value

    @staticmethod
    def _validate_name(value) -> bool:
        """
        Валидация наименования детали.

        Правила:
        - Строка от 1 до 100 символов
        - Может содержать: буквы (любые), цифры, пробелы, дефисы, скобки
        - Примеры: "Фильтр масляный", "Тормозные колодки", "Oil Filter (OEM)"

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        if not isinstance(value, str):
            return False

        # Название: любые буквы, цифры, пробелы, дефисы, скобки, слеши
        pattern = r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-\(\)\/]+$"
        return 1 <= len(value) <= 100 and bool(re.match(pattern, value))
