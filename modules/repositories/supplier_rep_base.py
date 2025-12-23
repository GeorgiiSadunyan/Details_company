from abc import ABC, abstractmethod
from typing import Any

from modules.models.supplier import Supplier
from modules.models.supplier_mini import SupplierMini


class supplier_rep_base(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: list[dict[str, Any]] = self._load_data()

    def _load_data(self) -> list[dict[str, Any]]:
        """Загрузка данных из файла"""

        try:
            with open(self.file_path, encoding="utf-8") as f:
                return self.load(f)
        except FileNotFoundError:
            return []

    def _save_data(self):
        """Сохранение данных в файл"""

        with open(self.file_path, "w", encoding="utf-8") as f:
            self.save(f)

    @abstractmethod
    def load(self, file) -> list[dict[str, Any]]:
        """Абстрактный метод загрузки данных из файла"""
        pass

    @abstractmethod
    def save(self, file):
        """Абстрактный метод сохранения данных в файл"""
        pass

    # a. Чтение всех значений из файла
    def get_all(self) -> list[Supplier]:
        return [Supplier(**item) for item in self.data]

    # b. Запись всех значений в файл
    def save_all(self, suppliers: list[Supplier]):
        self.data = [s.to_dict(s.supplier_id) for s in suppliers]
        self._save_data()

    # c. Получить объект по ID
    def get_by_id(self, supplier_id: int) -> Supplier | None:
        for item in self.data:
            if item["supplier_id"] == supplier_id:
                return Supplier(**item)
        return None

    # d. Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k: int, n: int) -> list[SupplierMini]:
        start = (k - 1) * n
        end = start + n
        sorted_data = sorted(self.data, key=lambda x: x["supplier_id"])
        items = sorted_data[start:end]
        return [SupplierMini(item["supplier_id"], item["name"]) for item in items]

    # e. Сортировать элементы по выбранному полю
    def sort_by_field(self, field: str):
        if field not in ["supplier_id", "name", "address", "phone"]:
            raise ValueError(f"Поле {field} не поддерживает сортировку")
        self.data.sort(key=lambda x: x.get(field) or "")
        self._save_data()

    # f. Добавить объект в список (с новым ID)
    def add(self, supplier: Supplier):
        # проверка на уникальность
        for item in self.data:
            existing_supplier = Supplier(**item)
            if existing_supplier == supplier:
                raise ValueError(
                    f"Поставщик уже существует! "
                    f"Имя: {supplier.name}, Тел: {supplier.phone}"
                )

        if not self.data:
            new_id = 1
        else:
            new_id = max(item["supplier_id"] for item in self.data) + 1
        supplier.supplier_id = new_id
        self.data.append(supplier.to_dict(supplier.supplier_id))
        self._save_data()

    # g. Заменить элемент списка по ID
    def replace_by_id(self, supplier_id: int, supplier: Supplier):
        for i, item in enumerate(self.data):
            if item["supplier_id"] == supplier_id:
                supplier.supplier_id = supplier_id
                self.data[i] = supplier.to_dict(supplier_id)
                self._save_data()
                return
        raise ValueError(f"Поставщик с ID {supplier_id} не найден")

    # h. Удалить элемент списка по ID
    def remove_by_id(self, supplier_id: int):
        for i, item in enumerate(self.data):
            if item["supplier_id"] == supplier_id:
                del self.data[i]
                self._save_data()
                return
        raise ValueError(f"Поставщик с ID {supplier_id} не найден")

    # i. Получить количество элементов
    def get_count(self) -> int:
        return len(self.data)
