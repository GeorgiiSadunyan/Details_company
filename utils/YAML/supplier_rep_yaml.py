import yaml
from typing import Any
from models.supplier import Supplier
from models.supplier_mini import SupplierMini


class Supplier_rep_yaml:
    
    '''Класс для работы с YAML'''
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: list[dict[str, Any]] = self._load_data()


    def _load_data(self) -> list[dict[str, Any]]:
        
        """Загрузить данные из YAML-файла"""
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data if data is not None else []
        except FileNotFoundError:
            return []


    def _save_data(self):
        
        """Сохранить данные в YAML-файл"""
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, allow_unicode=True)


    # a. Чтение всех значений из файла
    def get_all(self) -> list[Supplier]:
        return [Supplier(**item) for item in self.data]


    # b. Запись всех значений в файл
    def save_all(self, suppliers: list[Supplier]):
        self.data = [s.to_dict() for s in suppliers]
        self._save_data()


    # c. Получить объект по ID
    def get_by_id(self, supplier_id: int) -> Supplier | None:
        for item in self.data:
            if item['supplier_id'] == supplier_id:
                return Supplier(**item)
        return None


    # d. Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k: int, n: int) -> list[SupplierMini]:
        start = (k-1) * n
        end = start + n
        # Сортируем по ID перед выборкой
        sorted_data = sorted(self.data, key=lambda x: x['supplier_id'])
        items = sorted_data[start:end]
        return [SupplierMini(item['supplier_id'], item['name']) for item in items]


    # e. Сортировать элементы по выбранному полю (например, name)
    def sort_by_field(self, field: str):
        if field not in ['supplier_id', 'name', 'phone', 'address']:
            raise ValueError(f"Поле {field} не поддерживается для сортировки")
        self.data.sort(key=lambda x: x.get(field) or '')
        self._save_data()


    # f. Добавить объект в список (с новым ID)
    def add(self, supplier: Supplier):
        if not self.data:
            new_id = 1
        else:
            new_id = max(item['supplier_id'] for item in self.data) + 1
        supplier.supplier_id = new_id
        self.data.append(supplier.to_dict())
        self._save_data()


    # g. Заменить элемент списка по ID
    def replace_by_id(self, supplier_id: int, supplier: Supplier):
        for i, item in enumerate(self.data):
            if item['supplier_id'] == supplier_id:
                supplier.supplier_id = supplier_id 
                self.data[i] = supplier.to_dict()
                self._save_data()
                return
        raise ValueError(f"Поставщик с ID {supplier_id} не найден")


    # h. Удалить элемент списка по ID
    def remove_by_id(self, supplier_id: int):
        for i, item in enumerate(self.data):
            if item['supplier_id'] == supplier_id:
                del self.data[i]
                self._save_data()
                return
        raise ValueError(f"Поставщик с ID {supplier_id} не найден")


    # i. Получить количество элементов
    def get_count(self) -> int:
        return len(self.data)