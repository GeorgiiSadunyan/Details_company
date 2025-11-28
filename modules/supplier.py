from modules.supplier_base import SupplierBase
from modules.supplier_mini import SupplierMini
import re


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
            
            elif len(args) in (2, 3, 4) and not kwargs:
                self._init_from_args(*args)
            
            else:
                raise ValueError("Неправильное количество аргументов!")
            
        elif kwargs:
            self._init_from_kwargs(kwargs)
        else:
            raise ValueError("Не переданы аргументы")
    
    
    '''Перегрузка конструктора'''
    
    
    def _init_from_args(self, *args):
        '''Из позиционных аргументов'''
        
        if len(args) == 2:
            # name, phone
            name, phone = args
            supplier_id = 0
            super().__init__(supplier_id, name)
            self.phone = phone
            self.address = None

        elif len(args) == 3:
            if isinstance(args[0], int):
                # supplier_id, name, address
                supplier_id, name, phone = args
                address = None
            else:
                name, phone, address = args
                supplier_id = 0
            super().__init__(supplier_id, name)
            self.phone = phone
            self.address = address

        elif len(args) == 4:
            # supplier_id, name, phone, address
            supplier_id, name, phone, address = args
            supplier_id = supplier_id
            super().__init__(supplier_id, name)
            self.phone = phone
            self.address = address
    
    
    def _init_from_dict(self, data: dict):
        '''Из словаря (JSON)'''
        
        try:
            supplier_id = data.get('supplier_id', 0) # может отсутствовать
            name = data['name']
            phone = data['phone']
            address = data.get('address') # может отсутствовать
        except KeyError as e:
            raise ValueError(f'Отсутствует необходимоее поле: {e}')
        
        super().__init__(supplier_id, name)
        self.phone = phone
        self.address = address
    
    
    def _init_from_string(self, csv_str: str):
        '''Из CSV или просто строки'''

        parts = [part.strip() for part in csv_str.split(',')]
        
        if len(parts) not in (2, 3, 4):
            raise ValueError('Строка ОБЯЗАТЕЛЬНО должна иметь '+
                             'наименование и телефон. ' +
                             'Опционально: id и адрес.')
        
        supplier_id, name, phone, address = [0, ' ', ' ', None]  
        
        if len(parts) == 2:
            if parts[0].isdigit():
                # id, name или id, phone
                raise ValueError('Обязательно укажите Имя и Телефон организации')
            name, phone = parts
            supplier_id = 0
            address = None
            
        elif len(parts) == 3:
            if parts[0].isdigit():
                # id, name, phone
                try:
                    supplier_id = int(parts[0])
                except ValueError:
                    raise ValueError("ID должен быть целым числом")
                name, phone = parts[1], parts[2]
            else:
                # name, phone, address
                name, phone, address = parts
                supplier_id = 0
            
        elif len(parts) == 4:
            try:
                supplier_id = int(parts[0])
            except ValueError:
                raise ValueError("ID должен быть целым числом")
            name, phone, address = parts[1], parts[2], parts[3]


        super().__init__(supplier_id, name)
        self.phone = phone
        self.address = address
    
    
    def _init_from_kwargs(self, kwargs: dict):
        '''Инициализация из kwargs''' 

        # Проверка обязательных полей
        required_fields = ['name', 'phone']
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(f"Отсутствуют обязательные поля: {', '.join(missing_fields)}")
        
        supplier_id = kwargs.get('supplier_id', 0)
        name = kwargs['name']
        phone = kwargs['phone']
        address = kwargs.get('address')
        
        super().__init__(supplier_id, name)
        self.phone = phone
        self.address = address
    
    
    
    
    '''поле address'''
    @property
    def address(self) -> str | None:
        return self._address
    
    @address.setter
    def address(self, value: str | None):
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
            raise ValueError(f"Некорректно набран номер! {value}")
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
        return (self._name == other._name and
                self._phone == other._phone)
        
        
    '''Преобразование полного Supplier в краткий SupplierMini'''
    def to_mini(self) -> 'SupplierMini':
        return SupplierMini(self._supplier_id, self._name)
    

    def to_dict(self, supplier_id: int) -> dict:
        return {
            "supplier_id": supplier_id,
            "name": self._name,
            "phone": self._phone,
            "address": self._address
        }