import re
from abc import ABC
from typing import Optional


class SupplierBase(ABC):
    def __init__(self, supplier_id: int, name: str):
        self.supplier_id = supplier_id
        self.name = name


    '''supplier_id: сеттер и валидация'''
    
    @property
    def supplier_id(self) -> int:
        return self._supplier_id
    
    @supplier_id.setter
    def supplier_id(self, value: int):
        if not self._validate_supplier_id(value):
            raise ValueError("ID поставщика должно" + 
                              "быть положительным целым числом!")
        self._supplier_id = value
        
    @staticmethod
    def _validate_supplier_id(value) -> bool:
        return isinstance(value, int) and value >= 0
    

    '''поле name: сеттер и валидация'''
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not self._validate_name(value):
            raise ValueError("Некорректное имя поставщика!")
        self._name = value
    
    @staticmethod
    def _validate_name(value) -> bool:
        pattern = r'^(?=.*[a-zA-Zа-яА-ЯёЁ])[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$'
        return isinstance(value, str) and 1 <= len(value) <= 100 and bool(re.match(pattern, value))
        
        
        
        

class Supplier(SupplierBase):
    '''Полная версия поставщика'''
    
    def __init__(self, *args, **kwargs):
                
        if args:
            if len(args) == 1 and not kwargs:
                arg = args[0] 
                if isinstance(arg, dict):
                    self._init_from_dict(arg)
                elif isinstance(arg, str):
                    self._init_from_string(arg)
                else:
                    raise ValueError("Hеподдерживаемый тип аргумента")
            
            elif len(args) in (3, 4) and not kwargs:
                self._init_from_args(*args)
            
            else:
                raise ValueError("Неправильное количество аргументов!")
            
        elif kwargs:
            self._init_from_kwargs(kwargs)
        else:
            raise ValueError("Не переданы аргументы")
    
    
    '''Перегрузка конструктора'''
    
    
    def _init_from_args(self, supplier_id, name, phone, address = None):
        '''Из позиционных аргументов'''
        
        super().__init__(supplier_id, name)
        self.phone = phone
        self.address = address
    
    
    def _init_from_dict(self, data: dict):
        '''Из словаря (JSON)'''
        
        try:
            supplier_id = data['supplier_id']
            name = data['name']
            phone = data['phone']
            address = data.get('address') #может отсутствовать
        except KeyError as e:
            raise ValueError(f'Отсутствует необходимоее поле: {e}')
        
        super().__init__(supplier_id, name)
        self.phone = phone
        self.address = address
    
    
    def _init_from_string(self, csv_str: str):
        '''Из CSV или просто строки'''

        parts = [part.strip() for part in csv_str.split(',')]
        
        if len(parts) not in (3, 4):
            raise ValueError('Строка ОБЯЗАТЕЛЬНО должна иметь '+
                             'id, наименование и телефон')
            
        try:
            supplier_id = int(parts[0])
        except ValueError:
            raise ValueError("ID должен быть целым числом")
        
        name = parts[1]
        phone = parts[-1]
        address = None
        
        if len(parts) == 4:
            adr = parts[2]
            address = adr if adr != '' else None

        super().__init__(supplier_id, name)
        self.phone = phone
        self.address = address
    
    
    def _init_from_kwargs(self, kwargs: dict):
        '''Инициализация из kwargs''' 

        # Проверка обязательных полей
        required_fields = ['supplier_id', 'name', 'phone']
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(f"Отсутствуют обязательные поля: {', '.join(missing_fields)}")
        
        supplier_id = kwargs['supplier_id']
        name = kwargs['name']
        phone = kwargs['phone']
        address = kwargs.get('address')
        
        super().__init__(supplier_id, name)
        self.phone = phone
        self.address = address
    
    
    '''поле address'''
    @property
    def address(self) -> Optional[str]:
        return self._address
    
    @address.setter
    def address(self, value: Optional[str]):
        if not self._validate_address(value):
            raise ValueError("Адрес слишком длинный! (>200 симоволов)")
        self._address = value
        
    @staticmethod
    def _validate_address(value) -> bool:
        if value is None:
            return True
        return isinstance(value, str) and len(value) <= 200
        
    
    '''поле phone'''
    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if not self._validate_phone(value):
            raise ValueError("Некорректно набран номер!")
        self._phone = value
    
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
        
    
    
    # Доп методы 
        
    def __str__(self):
        return (f"( ID = {self._supplier_id}, "
                f"Наименование = '{self._name}', Адрес = '{self._address}', "
                f"Телефон = '{self._phone}' )" )
        
    
    def __eq__(self, other):
        if not isinstance(other, Supplier):
            return False
        return (self._supplier_id == other._supplier_id and
                self._name == other._name and
                self._phone == other._phone)
        
        
    '''Преобразование полного Supplier в краткий SupplierMini'''
    def to_mini(self) -> 'SupplierMini':
        return SupplierMini(self._supplier_id, self._name)
    
        




'''Класс, содержащий только имя поставщика и его id'''
class SupplierMini(SupplierBase):
    
    def __init__(self, *args, **kwargs):
        if args:
            if len(args) == 1:
                arg = args[0]
                if isinstance(arg, dict):
                    self._init_from_dict(arg)
                elif isinstance(arg, str):
                    self._init_from_string(arg)
                else:
                    raise ValueError("Неподдерживаемый тип аргумента. "+
                                     "Ожидается dict или str")
                    
            elif len(args) == 2:
                # Два аргумента
                super().__init__(args[0], args[1])
                
            else:
                raise ValueError("Слишком много позиционных аргументов."+
                                "Максимум 2: supplier_id, name")
        elif kwargs:
            self._init_from_kwargs(kwargs)
        else:
            raise ValueError("Не переданы аргументы")
    
    # Перегрузка конструктора
    
    def _init_from_dict(self, data: dict):
        try:
            supplier_id = data['supplier_id']
            name = data['name']
        except KeyError as e:
            raise ValueError(f'Отсутствует необходимое поле: {e}')
        
        super().__init__(supplier_id, name)
    
    
    def _init_from_string(self, csv_str: str):
        
        parts = [part.strip() for part in csv_str.split(',')]
        
        if len(parts) != 2:
            raise ValueError('Строка ОБЯЗАТЕЛЬНО должна иметь '+
                             'id и наименование')
            
        try:
            supplier_id = int(parts[0])
        except ValueError:
            raise ValueError("id должен быть целым числом")
        
        name = parts[1]
        if not name:
            raise ValueError("Вы не ввели наименование!")
        
        super().__init__(supplier_id, name)

    def _init_from_kwargs(self, kwargs: dict):
        # Проверка обязательных полей
        required_fields = ['supplier_id', 'name']
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(f"Отсутствуют обязательные поля: {', '.join(missing_fields)}")
        
        supplier_id = kwargs['supplier_id']
        name = kwargs['name']
        
        super().__init__(supplier_id, name)
        
        
    
    
    def __str__(self) -> str:
        return f"Поставщик: {self._name} (id: {self._supplier_id})"
       
    
    '''Cравнение двух объектов по данным, а не по их местоположению в памяти'''
    def __eq__(self, other):
        if not isinstance(other, SupplierMini):
            return False
        return (self._supplier_id == other._supplier_id and
                self._name == other._name)