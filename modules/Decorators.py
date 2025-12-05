from modules.supplier_mini import SupplierMini
from modules.supplier_rep_DB import Supplier_rep_DB


class SupplierDB_FilterSort_Decorator:
    def __init__(self, repo):
        self.repo: Supplier_rep_DB = repo


    def get_k_n_short_list(
        self,
        k: int,
        n: int,
        filter_field: str | None = None, 
        filter_value: str | None = None,
        sort_field: str = 'supplier_id'
            ) -> list[SupplierMini]:
        query = "SELECT supplier_id, name FROM suppliers"
        params = []
        
        
        '''
        Метод для получения списка по номеру страницы и количеству элементов
        
        k: int,                           # номер страницы 
        n: int,                           # размер страницы 
        filter_field: str | None = None,  # поле, по которому фильтруем (например, 'name')
        filter_value: str | None = None,  # значение, по которому фильтруем (например, 'Тест')
        sort_field: str = 'supplier_id'   # поле, по которому сортируем (по умолчанию 'supplier_id')
        '''
        
        
        # Добавляем фильтр, если указан
        if filter_field and filter_value:
            if filter_field not in ['name', 'phone', 'address']:
                raise ValueError(f"Поле {filter_field} не поддерживается для фильтрации")
            query += f" WHERE {filter_field} = %s"
            params.append(filter_value)

        # Сорттировка
        if sort_field not in ['supplier_id', 'name', 'phone', 'address']:
            raise ValueError(f"Поле {sort_field} не поддерживается для сортировки")
        query += f" ORDER BY {sort_field}"

        offset = (k - 1) * n
        query += " LIMIT %s OFFSET %s;"
        params.extend([n, offset])

        result = self.repo.db._execute_query(query, tuple(params))
        return [SupplierMini(supplier_id=row[0], name=row[1]) for row in result]


    def get_count(self, filter_field: str | None = None, filter_value: str | None = None) -> int:
        
        '''
        Метод для получения числа элементов с одинаковыми значениями
    
        '''
        
        query = "SELECT COUNT(*) FROM suppliers"
        params = []

        if filter_field and filter_value:
            if filter_field not in ['name', 'phone', 'address']:
                raise ValueError(f"Поле {filter_field} не поддерживается для фильтрации")
            query += f" WHERE {filter_field} = %s"
            params.append(filter_value)

        query += ";"
        result = self.repo.db._execute_query(query, tuple(params))
        return result[0][0]
    
    def close(self):
        self.repo.close()