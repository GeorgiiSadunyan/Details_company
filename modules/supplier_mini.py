from models.supplier_base import SupplierBase


class SupplierMini(SupplierBase):
    
    '''Класс, содержащий только имя поставщика и его id'''
    
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
       
    
    def __eq__(self, other):
        
        '''Cравнение двух объектов по данным, а не по их местоположению в памяти'''

        if not isinstance(other, SupplierMini):
            return False
        return (self._supplier_id == other._supplier_id and
                self._name == other._name)
        
        
    def to_dict(self) -> dict:
        
        '''Преобразование в словарь'''
        
        return {
            "supplier_id": self._supplier_id,
            "name": self._name,
        }