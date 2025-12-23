from abc import ABC


class PurchaseBase(ABC):
    """
    Абстрактный базовый класс для закупки.
    Определяет общие атрибуты и методы валидации для всех типов закупок.

    Attributes:
        purchase_id (int | None): Уникальный идентификатор закупки
        article (str): Артикул детали
        quantity (int): Количество закупленных единиц
    """

    def __init__(
        self,
        article: str,
        quantity: int,
        purchase_id: int | None = None,
    ):
        """
        Инициализация PurchaseBase.

        Args:
            article (str): Артикул детали
            quantity (int): Количество единиц
            purchase_id (int | None): ID закупки (опциональный, по умолчанию None)
        """
        self.purchase_id = purchase_id
        self.article = article
        self.quantity = quantity

    # ==================== PURCHASE_ID ====================

    @property
    def purchase_id(self) -> int | None:
        """Геттер для ID закупки."""
        return self._purchase_id

    @purchase_id.setter
    def purchase_id(self, value: int | None):
        """
        Сеттер для ID закупки с валидацией.

        Args:
            value (int | None): ID закупки (None для новых записей)

        Raises:
            ValueError: Некорректный ID закупки
        """
        if not self._validate_purchase_id(value):
            raise ValueError(
                f"Некорректный ID закупки: '{value}'. "
                "ID должен быть неотрицательным целым числом или None."
            )
        self._purchase_id = value

    @staticmethod
    def _validate_purchase_id(value) -> bool:
        """
        Валидация ID закупки.

        Правила:
        - Может быть None (для новых записей)
        - Или целое число, неотрицательное (>= 0)

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        if value is None:
            return True
        return isinstance(value, int) and value >= 0

    # ==================== ARTICLE ====================

    @property
    def article(self) -> str:
        """Геттер для артикула."""
        return self._article

    @article.setter
    def article(self, value: str):
        """
        Сеттер для артикула с валидацией.

        Args:
            value (str): Артикул детали

        Raises:
            ValueError: Некорректный артикул
        """
        if not self._validate_article(value):
            raise ValueError(
                f"Некорректный артикул: '{value}'. "
                "Артикул должен содержать от 1 до 50 символов."
            )
        self._article = value

    @staticmethod
    def _validate_article(value) -> bool:
        """
        Валидация артикула.

        Правила:
        - Строка
        - От 1 до 50 символов

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        return isinstance(value, str) and 1 <= len(value) <= 50

    # ==================== QUANTITY ====================

    @property
    def quantity(self) -> int:
        """Геттер для количества."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        """
        Сеттер для количества с валидацией.

        Args:
            value (int): Количество единиц

        Raises:
            ValueError: Некорректное количество
        """
        if not self._validate_quantity(value):
            raise ValueError(
                f"Некорректное количество: '{value}'. "
                "Количество должно быть положительным целым числом от 1 до 10000."
            )
        self._quantity = value

    @staticmethod
    def _validate_quantity(value) -> bool:
        """
        Валидация количества.

        Правила:
        - Целое число
        - От 1 до 10000

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        return isinstance(value, int) and 1 <= value <= 10000
