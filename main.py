import re
from typing import Optional


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
        # (123) 456-7890        
        return bool(re.match(mask, value.strip())) if value.strip() else False
    
    
    
    # Доп методы для красивого вывода Объектов и их сравнения
    
    def __repr__(self):
        return (f"Поставщик( ID = {self._supplier_id}, "
                f"Наименование = '{self._name}', Адрес = '{self._address}', "
                f"Телефон = '{self._phone}' )" )
        
    
    # сравнение двух объектов по данным, а не по их местоположению в памяти
    def __eq__(self, other):
        if not isinstance(other, Supplier):
            return False
        return (self._supplier_id == other._supplier_id and
                self._name == other._name and
                self._address == other._address and
                self._phone == other._phone)
    




# Успешное создание
try:
    s1 = Supplier(
        supplier_id=1,
        name="АвтоДеталь ООО",
        address= "Москва, Тверская 10",
        phone="+7 (999) 123-45-67"
    )
    print(s1)
except ValueError as e:
    print("Ошибка:", e)