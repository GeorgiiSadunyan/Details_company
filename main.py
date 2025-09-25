import re
from typing import Optional, Any


class Supplier:
    def __init__(self, 
                 supplier_id: int, 
                 name: str, 
                 phone: str,
                 address: Optional[str] = None, ):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.phone = phone
        
    
    @property
    def supplier_id(self) -> int:
        return self._supplier_id
    
    @supplier_id.setter
    def supplier_id(self, value: int):
        if not self._validate_supplier_id(value):
            raise ValueError("ID поставщика должно" + 
                              "быть положительным целым числом!")
        self._supplier_id = value
        
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not self._validate_name(value):
            raise ValueError("Вы не ввели имя поставщика!")
        self._name = value
        
    
    @property
    def address(self) -> Optional[str]:
        return self._address
    
    @address.setter
    def address(self, value: Optional[str]):
        if not self._validate_address(value):
            raise ValueError("Адрес слишком длинный! (>200 симоволов)")
        self._address = value
        
    
    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if not self._validate_phone(value):
            raise ValueError("Некорректно набран номер!")
        self._phone = value
        
        
        
    # Валидация
    
    @staticmethod
    def _validate_supplier_id(value) -> bool:
        return isinstance(value, int) and value > 0
    
    @staticmethod
    def _validate_name(value) -> bool:
        return isinstance(value, str) and 1 <= len(value) <= 100
    
    @staticmethod
    def _validate_address(value) -> bool:
        if value is None:
            return True
        return isinstance(value, str) and len(value) <= 200
    
    @staticmethod
    def _validate_phone(value) -> bool:
        if not isinstance(value, str):
            return False
        
        mask = r'^[\+]?[78]?[\s\-]?[\(]?\d{3}[\)]?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
        # Регулярное выражение для СНГ номеров
        # Примеры допустимых форматов:
        # +7 (999) 123-45-67
        # 89991234567
        return bool(re.match(mask, value.strip())) if value.strip() else False
    
    
    
    # Перегрузка конструктора
    
    # из словаря (JSON)
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Supplier':
        try:
            return cls(
                supplier_id = data['supplier_id'],
                name = data['name'],
                phone = data['phone'],
                address = data.get('address') #может отсутствовать
            )
        except KeyError as e:
            raise ValueError(f'Отсутствует необходимоее поле: {e}')
        except TypeError as e:
            raise ValueError(f'Неправильный тип данных: {e}')
    
    
    # Из CSV или просто строки
    @classmethod
    def from_csv_string(cls, csv_str: str) -> 'Supplier':
        """_summary_
        Args:
            csv_str (str): строка вида id,name,address,phone
        Returns:
            Supplier: _description_
        """
        parts = [part.strip() for part in csv_str.split(',')]
        if len(parts) not in (3, 4):
            raise ValueError('Строка ОБЯЗАТЕЛЬНО должна иметь '+
                             'id, наименование, телефон')
            
        supplier_id = int(parts[0])
        name = parts[1]
        phone = parts[-1]
        address = None
        if len(parts) == 4:
            adr = parts[2] # там может ничего не быть (,,)
            address = adr if adr!='' else None

        return cls(
            supplier_id=supplier_id,
            name = name,
            phone = phone,
            address = address
        )
        
        

    
    # Доп методы для красивого вывода Объектов и их сравнения
    
    
    '''Краткая версия'''
    def __str__(self) -> str:
        return f"Поставщик: {self._name} (id: {self._supplier_id})"
    
    
    '''Полный вывод информации об объекте'''
    def __repr__(self):
        return (f"( ID = {self._supplier_id}, "
                f"Наименование = '{self._name}', Адрес = '{self._address}', "
                f"Телефон = '{self._phone}' )" )
        
    
    '''Cравнение двух объектов по данным, а не по их местоположению в памяти'''
    def __eq__(self, other):
        if not isinstance(other, Supplier):
            return False
        return (self._supplier_id == other._supplier_id and
                self._name == other._name and
                self._address == other._address and
                self._phone == other._phone)