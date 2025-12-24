from datetime import date, datetime

from modules.models.purchase_base import PurchaseBase
from modules.models.purchase_mini import PurchaseMini


class Purchase(PurchaseBase):
    """
    Полная версия закупки.

    Attributes:
        purchase_id (int | None): ID закупки (опциональный)
        supplier_id (int): ID поставщика
        article (str): Артикул детали
        quantity (int): Количество единиц
        purchase_date (date): Дата закупки
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация Purchase.

        Поддерживаемые форматы:
        1. Purchase(supplier_id, article, quantity, purchase_date) - без ID
        2. Purchase(purchase_id, supplier_id, article, quantity, purchase_date) - с ID
        3. Purchase({"supplier_id": ..., "article": ..., ...}) - словарь
        4. Purchase("5, FLT-001, 100, 2025-12-23") - CSV без ID
        5. Purchase("1, 5, FLT-001, 100, 2025-12-23") - CSV с ID
        6. Purchase(supplier_id=..., article=..., ...) - kwargs

        Args:
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы

        Raises:
            ValueError: Некорректные аргументы
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

            elif len(args) == 4 and not kwargs:
                # supplier_id, article, quantity, purchase_date (без purchase_id)
                supplier_id, article, quantity, purchase_date = args
                super().__init__(article, quantity, purchase_id=None)
                self.supplier_id = supplier_id
                self.purchase_date = purchase_date

            elif len(args) == 5 and not kwargs:
                # purchase_id, supplier_id, article, quantity, purchase_date
                purchase_id, supplier_id, article, quantity, purchase_date = args
                super().__init__(article, quantity, purchase_id)
                self.supplier_id = supplier_id
                self.purchase_date = purchase_date

            else:
                raise ValueError("Неправильное количество аргументов!")

        elif kwargs:
            self._init_from_kwargs(kwargs)
        else:
            raise ValueError("Не переданы аргументы")

    # ==================== ПЕРЕГРУЗКА КОНСТРУКТОРА ====================

    def _init_from_dict(self, data: dict):
        """
        Инициализация из словаря.

        Args:
            data (dict): Словарь с полями

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        try:
            supplier_id = data["supplier_id"]
            article = data["article"]
            quantity = data["quantity"]
            purchase_date = data["purchase_date"]
        except KeyError as e:
            raise ValueError(f"Отсутствует необходимое поле: {e}")

        purchase_id = data.get("purchase_id")  # Опциональное поле
        super().__init__(article, quantity, purchase_id)
        self.supplier_id = supplier_id
        self.purchase_date = purchase_date

    def _init_from_string(self, csv_str: str):
        """
        Инициализация из CSV-строки.

        Формат 1: "supplier_id, article, quantity, date" - без purchase_id
        Формат 2: "purchase_id, supplier_id, article, quantity, date" - с purchase_id

        Args:
            csv_str (str): CSV-строка

        Raises:
            ValueError: Некорректный формат
        """
        parts = [part.strip() for part in csv_str.split(",")]

        if len(parts) == 4:
            # Без purchase_id: supplier_id, article, quantity, date
            try:
                supplier_id = int(parts[0])
                article = parts[1]
                quantity = int(parts[2])
                purchase_date = parts[3]
            except ValueError as e:
                raise ValueError(f"Ошибка парсинга: {e}")
            super().__init__(article, quantity, purchase_id=None)
            self.supplier_id = supplier_id
            self.purchase_date = purchase_date
        elif len(parts) == 5:
            # С purchase_id: purchase_id, supplier_id, article, quantity, date
            try:
                purchase_id = int(parts[0])
                supplier_id = int(parts[1])
                article = parts[2]
                quantity = int(parts[3])
                purchase_date = parts[4]
            except ValueError as e:
                raise ValueError(f"Ошибка парсинга: {e}")
            super().__init__(article, quantity, purchase_id)
            self.supplier_id = supplier_id
            self.purchase_date = purchase_date
        else:
            raise ValueError(
                "Строка должна содержать 4 поля (supplier_id, article, quantity, date) "
                "или 5 полей (purchase_id, supplier_id, article, quantity, date)"
            )

    def _init_from_kwargs(self, kwargs: dict):
        """
        Инициализация из именованных аргументов.

        Args:
            kwargs (dict): Словарь аргументов

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        required_fields = ["supplier_id", "article", "quantity", "purchase_date"]
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(
                f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
            )

        supplier_id = kwargs["supplier_id"]
        article = kwargs["article"]
        quantity = kwargs["quantity"]
        purchase_date = kwargs["purchase_date"]
        purchase_id = kwargs.get("purchase_id")  # Опциональное поле

        super().__init__(article, quantity, purchase_id)
        self.supplier_id = supplier_id
        self.purchase_date = purchase_date

    # ==================== SUPPLIER_ID ====================

    @property
    def supplier_id(self) -> int:
        """Геттер для ID поставщика."""
        return self._supplier_id

    @supplier_id.setter
    def supplier_id(self, value: int):
        """
        Сеттер для ID поставщика с валидацией.

        Args:
            value (int): ID поставщика

        Raises:
            ValueError: Некорректный ID поставщика
        """
        if not self._validate_supplier_id(value):
            raise ValueError(
                f"Некорректный ID поставщика: '{value}'. "
                "ID должен быть положительным целым числом."
            )
        self._supplier_id = value

    @staticmethod
    def _validate_supplier_id(value) -> bool:
        """
        Валидация ID поставщика.

        Правила:
        - Целое число
        - Положительное (> 0)

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        return isinstance(value, int) and value > 0

    # ==================== PURCHASE_DATE ====================

    @property
    def purchase_date(self) -> date:
        """Геттер для даты закупки."""
        return self._purchase_date

    @purchase_date.setter
    def purchase_date(self, value: date | str):
        """
        Установка даты закупки с валидацией.

        Args:
            value: Дата (date, datetime или строка в формате YYYY-MM-DD)

        Raises:
            ValueError: Некорректная дата
        """
        if not self._validate_purchase_date(value):
            raise ValueError(
                f"Некорректная дата закупки: '{value}'. "
                "Дата не может быть в будущем."
            )

        # Преобразуем в date
        if isinstance(value, date):
            self._purchase_date = value
        elif isinstance(value, datetime):
            self._purchase_date = value.date()
        elif isinstance(value, str):
            try:
                self._purchase_date = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    f"Некорректный формат даты: '{value}'. "
                    "Ожидается формат YYYY-MM-DD."
                )
        else:
            raise TypeError(f"Неподдерживаемый тип для даты: {type(value)}")

    @staticmethod
    def _validate_purchase_date(value) -> bool:
        """
        Валидация даты закупки.

        Правила:
        - Дата не может быть в будущем
        - Поддерживаются типы: date, datetime, str (YYYY-MM-DD)

        Args:
            value: Значение для проверки

        Returns:
            bool: True если валидно, False иначе
        """
        try:
            if isinstance(value, date):
                purchase_date = value
            elif isinstance(value, datetime):
                purchase_date = value.date()
            elif isinstance(value, str):
                purchase_date = datetime.strptime(value, "%Y-%m-%d").date()
            else:
                return False

            # Проверка: дата не в будущем
            if purchase_date > date.today():
                return False

            return True

        except (ValueError, TypeError):
            return False


    # ==================== МЕТОДЫ ====================

    def __str__(self) -> str:
        return (
            f"Purchase(purchase_id={self._purchase_id}, "
            f"supplier_id={self._supplier_id}, "
            f"article='{self._article}', "
            f"quantity={self._quantity}, "
            f"purchase_date='{self._purchase_date}')"
        )


    def to_mini(self) -> PurchaseMini:
        """
        Преобразование полного Purchase в краткий PurchaseMini.

        Returns:
            PurchaseMini: Краткая версия закупки
        """
        return PurchaseMini(
            self._purchase_id,
            self._article,
            self._quantity,
        )

    def to_dict(self) -> dict:
        """
        Преобразование в словарь.

        Returns:
            dict: Словарь с полями закупки
        """
        result = {
            "supplier_id": self._supplier_id,
            "article": self._article,
            "quantity": self._quantity,
            "purchase_date": self._purchase_date.isoformat(),  # Для JSON
        }
        if self._purchase_id is not None:
            result["purchase_id"] = self._purchase_id
        return result
