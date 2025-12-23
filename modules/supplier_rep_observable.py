"""
Observable репозиторий поставщиков
Уведомляет наблюдателей об изменениях в данных
"""

from modules.observer import Subject
from modules.supplier import Supplier
from modules.supplier_mini import SupplierMini
from modules.supplier_rep_base import supplier_rep_base


class SupplierRepObservable(Subject):
    """
    Обёртка над репозиторием поставщиков с поддержкой паттерна Observer
    """

    def __init__(self, repository: supplier_rep_base):
        super().__init__()
        self.repository = repository

    def get_all(self) -> list[Supplier]:
        """Получить всех поставщиков"""
        suppliers = self.repository.get_all()
        self.notify("data_loaded", suppliers)
        return suppliers

    def get_by_id(self, supplier_id: int) -> Supplier | None:
        """Получить поставщика по ID"""
        supplier = self.repository.get_by_id(supplier_id)
        if supplier:
            self.notify("item_selected", supplier)
        return supplier

    def get_k_n_short_list(self, k: int, n: int) -> list[SupplierMini]:
        """Получить список k по счету n объектов класса short"""
        short_list = self.repository.get_k_n_short_list(k, n)
        self.notify("short_list_loaded", {"items": short_list, "page": k, "size": n})
        return short_list

    def add(self, supplier: Supplier):
        """Добавить поставщика"""
        self.repository.add(supplier)
        self.notify("item_added", supplier)

    def replace_by_id(self, supplier_id: int, supplier: Supplier):
        """Заменить поставщика по ID"""
        self.repository.replace_by_id(supplier_id, supplier)
        self.notify("item_updated", supplier)

    def remove_by_id(self, supplier_id: int):
        """Удалить поставщика по ID"""
        self.repository.remove_by_id(supplier_id)
        self.notify("item_deleted", supplier_id)

    def get_count(self) -> int:
        """Получить количество элементов"""
        return self.repository.get_count()

    def sort_by_field(self, field: str):
        """Сортировать по полю"""
        self.repository.sort_by_field(field)
        self.notify("data_sorted", field)
