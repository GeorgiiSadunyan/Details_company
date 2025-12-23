from modules.models.purchase_base import PurchaseBase


class PurchaseMini(PurchaseBase):
    """
    Краткая версия закупки.
    Используется для отображения в списках и таблицах.

    Attributes:
        purchase_id (int | None): ID закупки (опциональный)
        article (str): Артикул детали
        quantity (int): Количество
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация PurchaseMini.

        Поддерживаемые форматы:
        1. PurchaseMini(article, quantity) - только обязательные поля
        2. PurchaseMini(purchase_id, article, quantity) - с ID
        3. PurchaseMini({"article": ..., "quantity": ..., "purchase_id": ...})
        4. PurchaseMini("FLT-001, 100") - CSV без ID
        5. PurchaseMini("1, FLT-001, 100") - CSV с ID
        6. PurchaseMini(article=..., quantity=..., purchase_id=...)

        Args:
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы

        Raises:
            ValueError: Некорректные аргументы
        """
        if args:
            if len(args) == 1:
                arg = args[0]
                if isinstance(arg, dict):
                    self._init_from_dict(arg)
                elif isinstance(arg, str):
                    self._init_from_string(arg)
                else:
                    raise ValueError(
                        "Неподдерживаемый тип аргумента. Ожидается dict или str"
                    )

            elif len(args) == 2:
                # article, quantity (без ID)
                article, quantity = args
                super().__init__(article, quantity)

            elif len(args) == 3:
                # purchase_id, article, quantity
                purchase_id, article, quantity = args
                super().__init__(article, quantity, purchase_id)

            else:
                raise ValueError(
                    "Некорректное количество аргументов. "
                    "Ожидается: (article, quantity)"
                    " или (purchase_id, article, quantity)"
                )
        elif kwargs:
            self._init_from_kwargs(kwargs)
        else:
            raise ValueError("Не переданы аргументы")

    # ==================== ПЕРЕГРУЗКА КОНСТРУКТОРА ====================

    def _init_from_dict(self, data: dict):
        """
        Инициализация из словаря.

        Args:
            data (dict): Словарь с полями article, quantity и опциональным purchase_id

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        try:
            article = data["article"]
            quantity = data["quantity"]
        except KeyError as e:
            raise ValueError(f"Отсутствует необходимое поле: {e}")

        purchase_id = data.get("purchase_id")  # Опциональное поле
        super().__init__(article, quantity, purchase_id)

    def _init_from_string(self, csv_str: str):
        """
        Инициализация из CSV-строки.

        Формат 1: "article, quantity" - без ID
        Формат 2: "purchase_id, article, quantity" - с ID
        Примеры:
        - "FLT-001, 100"
        - "1, FLT-001, 100"

        Args:
            csv_str (str): CSV-строка

        Raises:
            ValueError: Некорректный формат
        """
        parts = [part.strip() for part in csv_str.split(",")]

        if len(parts) == 2:
            # Без ID: article, quantity
            article = parts[0]
            quantity = int(parts[1])
            super().__init__(article, quantity)
        elif len(parts) == 3:
            # С ID: purchase_id, article, quantity
            try:
                purchase_id = int(parts[0])
                article = parts[1]
                quantity = int(parts[2])
            except ValueError as e:
                raise ValueError(f"Ошибка парсинга данных: {e}")
            super().__init__(article, quantity, purchase_id)
        else:
            raise ValueError(
                "Строка должна содержать 2 поля (article, quantity) "
                "или 3 поля (purchase_id, article, quantity)"
            )

    def _init_from_kwargs(self, kwargs: dict):
        """
        Инициализация из именованных аргументов.

        Args:
            kwargs (dict): Словарь аргументов

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        required_fields = ["article", "quantity"]
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(
                f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
            )

        article = kwargs["article"]
        quantity = kwargs["quantity"]
        purchase_id = kwargs.get("purchase_id")  # Опциональное поле

        super().__init__(article, quantity, purchase_id)

    # ==================== МЕТОДЫ ====================

    def __str__(self) -> str:
        return (
            f"PurchaseMini(purchase_id={self._purchase_id}, "
            f"article='{self._article}', "
            f"quantity={self._quantity})"
        )


    def to_dict(self) -> dict:
        """
        Преобразование в словарь.

        Returns:
            dict: Словарь с полями закупки
        """
        result = {
            "article": self._article,
            "quantity": self._quantity,
        }
        if self._purchase_id is not None:
            result["purchase_id"] = self._purchase_id
        return result
