import re
from abc import ABC


class SupplierBase(ABC):
    def __init__(self, supplier_id: int, name: str):
        self.supplier_id = supplier_id
        self.name = name

    """supplier_id: сеттер и валидация"""

    @property
    def supplier_id(self) -> int:
        return self._supplier_id

    @supplier_id.setter
    def supplier_id(self, value: int):
        if not self._validate_supplier_id(value):
            raise ValueError(
                "ID поставщика должно" + "быть положительным целым числом!"
            )
        self._supplier_id = value

    @staticmethod
    def _validate_supplier_id(value) -> bool:
        return isinstance(value, int) and value >= 0

    """поле name: сеттер и валидация"""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not self._validate_name(value):
            raise ValueError(f"Некорректное имя поставщика! {value}")
        self._name = value

    @staticmethod
    def _validate_name(value) -> bool:
        pattern = r"^(?=.*[a-zA-Zа-яА-ЯёЁ])[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$"
        return (
            isinstance(value, str)
            and 1 <= len(value) <= 100
            and bool(re.match(pattern, value))
        )
