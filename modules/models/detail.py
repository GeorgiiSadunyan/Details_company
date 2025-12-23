"""
Полная версия детали (запчасти).
Содержит артикул, наименование и цену.
"""

from decimal import Decimal, InvalidOperation

from modules.models.detail_base import DetailBase
from modules.models.detail_mini import DetailMini


class Detail(DetailBase):
    """
    Полная версия детали.

    Attributes:
        article (str): Артикул детали (уникальный идентификатор)
        name (str): Наименование детали
        price (Decimal): Цена за единицу (руб.)
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация Detail.

        Поддерживаемые форматы:
        1. Detail(article, name, price) - позиционные аргументы
        2. Detail({"article": "...", "name": "...", "price": ...}) - словарь
        3. Detail("FLT-001, Фильтр масляный, 500.00") - CSV-строка
        4. Detail(article="...", name="...", price=...) - именованные аргументы

        Args:
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы

        Raises:
            ValueError: Некорректные аргументы или отсутствуют обязательные поля
        """
        if args:
            if len(args) == 1 and not kwargs:
                arg = args[0]
                if isinstance(arg, dict):
                    self._init_from_dict(arg)
                elif isinstance(arg, str):
                    self._init_from_string(arg)
                else:
                    raise ValueError("Неподдерживаемый тип аргумента")

            elif len(args) == 2 and not kwargs:
                # article, name (цена по умолчанию = 0)
                article, name = args
                super().__init__(article, name)
                self.price = Decimal("0.00")

            elif len(args) == 3 and not kwargs:
                # article, name, price
                article, name, price = args
                super().__init__(article, name)
                self.price = price

            else:
                raise ValueError("Неправильное количество аргументов!")

        elif kwargs:
            self._init_from_kwargs(kwargs)
        else:
            raise ValueError("Не переданы аргументы")

    # ==================== ПЕРЕГРУЗКА КОНСТРУКТОРА ====================

    def _init_from_dict(self, data: dict):
        """
        Инициализация из словаря (например, JSON).

        Args:
            data (dict): Словарь с полями article, name, price

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        try:
            article = data["article"]
            name = data["name"]
            price = data["price"]
        except KeyError as e:
            raise ValueError(f"Отсутствует необходимое поле: {e}")

        super().__init__(article, name)
        self.price = price

    def _init_from_string(self, csv_str: str):
        """
        Инициализация из CSV-строки.

        Формат: "article, name, price"
        Пример: "FLT-001, Фильтр масляный, 500.00"

        Args:
            csv_str (str): CSV-строка

        Raises:
            ValueError: Некорректный формат строки
        """
        parts = [part.strip() for part in csv_str.split(",")]

        if len(parts) not in (2, 3):
            raise ValueError(
                "Строка должна содержать артикул, наименование "
                "и опционально цену. Формат: 'article, name, price'"
            )

        article = parts[0]
        name = parts[1]
        price = Decimal("0.00")

        if not article:
            raise ValueError("Артикул не может быть пустым!")
        if not name:
            raise ValueError("Наименование не может быть пустым!")

        if len(parts) == 3:
            try:
                price = Decimal(parts[2])
            except (ValueError, InvalidOperation):
                raise ValueError(f"Некорректная цена: '{parts[2]}'. Ожидается число.")

        super().__init__(article, name)
        self.price = price

    def _init_from_kwargs(self, kwargs: dict):
        """
        Инициализация из именованных аргументов.

        Args:
            kwargs (dict): Словарь с именованными аргументами

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        # Проверка обязательных полей
        required_fields = ["article", "name", "price"]
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(
                f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
            )

        article = kwargs["article"]
        name = kwargs["name"]
        price = kwargs["price"]

        super().__init__(article, name)
        self.price = price

    # ==================== PRICE ====================

    @property
    def price(self) -> Decimal:
        """Цена за единицу (руб.)"""
        return self._price

    @price.setter
    def price(self, value):
        """
        Установка цены с валидацией.

        Args:
            value: Цена (может быть Decimal, float, int или str)

        Raises:
            ValueError: Некорректная цена
        """
        if not self._validate_price(value):
            raise ValueError(
                f"Некорректная цена: '{value}'. "
                "Цена должна быть неотрицательным числом от 0.00 до 999,999.99 руб."
            )

        # Преобразуем в Decimal
        if isinstance(value, Decimal):
            self._price = value
        elif isinstance(value, (int, float)):
            self._price = Decimal(str(value))
        elif isinstance(value, str):
            try:
                self._price = Decimal(value)
            except InvalidOperation:
                raise ValueError(f"Невозможно преобразовать '{value}' в число")
        else:
            raise ValueError(f"Неподдерживаемый тип для цены: {type(value)}")

    @staticmethod
    def _validate_price(value) -> bool:
        """
        Валидация цены.

        Правила:
        - Неотрицательное число (может быть 0 для новых записей)
        - От 0.00 до 999,999.99
        - Максимум 2 знака после запятой (DECIMAL(10,2))

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        try:
            if isinstance(value, str):
                price = Decimal(value)
            elif isinstance(value, (int, float, Decimal)):
                price = Decimal(str(value))
            else:
                return False

            # Проверка диапазона (разрешаем 0 для новых записей)
            if price < Decimal("0.00") or price > Decimal("999999.99"):
                return False

            # Проверка количества знаков после запятой (максимум 2)
            # Decimal('123.456').as_tuple().exponent вернет -3
            if price.as_tuple().exponent < -2:  # type: ignore
                return False

            return True

        except (ValueError, InvalidOperation):
            return False

    # ==================== МЕТОДЫ ====================

    def __str__(self) -> str:
        """Строковое представление"""
        return (
            f"Деталь: {self._name} "
            f"(артикул: {self._article}, цена: {self._price:.2f} ₽)"
        )

    def __eq__(self, other) -> bool:
        """
        Сравнение двух объектов по данным.

        Args:
            other: Объект для сравнения

        Returns:
            bool: True если объекты равны по данным
        """
        if not isinstance(other, Detail):
            return False
        return (
            self._article == other._article
            and self._name == other._name
            and self._price == other._price
        )

    def to_mini(self) -> DetailMini:
        """
        Преобразование полного Detail в краткий DetailMini.

        Returns:
            DetailMini: Краткая версия детали
        """
        return DetailMini(self._article, self._name)

    def to_dict(self) -> dict:
        """
        Преобразование в словарь.

        Returns:
            dict: Словарь с полями article, name, price
        """
        return {
            "article": self._article,
            "name": self._name,
            "price": float(self._price),  # Для JSON-сериализации
        }
