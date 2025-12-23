"""
Краткая версия детали (запчасти).
Содержит только артикул и наименование.
"""

from modules.models.detail_base import DetailBase


class DetailMini(DetailBase):
    """
    Краткая версия детали (short-версия).
    Используется для отображения в списках и таблицах.

    Attributes:
        article (str): Артикул детали
        name (str): Наименование детали
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация DetailMini.

        Поддерживаемые форматы:
        1. DetailMini(article, name) - позиционные аргументы
        2. DetailMini({"article": "...", "name": "..."}) - словарь
        3. DetailMini("FLT-001, Фильтр масляный") - CSV-строка
        4. DetailMini(article="...", name="...") - именованные аргументы

        Args:
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы

        Raises:
            ValueError: Некорректные аргументы или отсутствуют обязательные поля
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
                # Два аргумента: article, name
                super().__init__(args[0], args[1])

            else:
                raise ValueError(
                    "Слишком много позиционных аргументов. Максимум 2: article, name"
                )
        elif kwargs:
            self._init_from_kwargs(kwargs)
        else:
            raise ValueError("Не переданы аргументы")

    # ==================== ПЕРЕГРУЗКА КОНСТРУКТОРА ====================

    def _init_from_dict(self, data: dict):
        """
        Инициализация из словаря (например, JSON).

        Args:
            data (dict): Словарь с полями article и name

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        try:
            article = data["article"]
            name = data["name"]
        except KeyError as e:
            raise ValueError(f"Отсутствует необходимое поле: {e}")

        super().__init__(article, name)

    def _init_from_string(self, csv_str: str):
        """
        Инициализация из CSV-строки.

        Формат: "article, name"
        Пример: "FLT-001, Фильтр масляный"

        Args:
            csv_str (str): CSV-строка

        Raises:
            ValueError: Некорректный формат строки
        """
        parts = [part.strip() for part in csv_str.split(",")]

        if len(parts) != 2:
            raise ValueError(
                "Строка ОБЯЗАТЕЛЬНО должна иметь артикул и наименование. "
                "Формат: 'article, name'"
            )

        article = parts[0]
        name = parts[1]

        if not article:
            raise ValueError("Артикул не может быть пустым!")
        if not name:
            raise ValueError("Наименование не может быть пустым!")

        super().__init__(article, name)

    def _init_from_kwargs(self, kwargs: dict):
        """
        Инициализация из именованных аргументов.

        Args:
            kwargs (dict): Словарь с именованными аргументами

        Raises:
            ValueError: Отсутствуют обязательные поля
        """
        # Проверка обязательных полей
        required_fields = ["article", "name"]
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(
                f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
            )

        article = kwargs["article"]
        name = kwargs["name"]

        super().__init__(article, name)

    # ==================== МЕТОДЫ ====================

    def __str__(self) -> str:
        """Строковое представление"""
        return f"Деталь: {self._name} (артикул: {self._article})"

    def __eq__(self, other) -> bool:
        """
        Сравнение двух объектов по данным.

        Args:
            other: Объект для сравнения

        Returns:
            bool: True если объекты равны по данным
        """
        if not isinstance(other, DetailMini):
            return False
        return self._article == other._article and self._name == other._name

    def to_dict(self) -> dict:
        """
        Преобразование в словарь.

        Returns:
            dict: Словарь с полями article и name
        """
        return {
            "article": self._article,
            "name": self._name,
        }
