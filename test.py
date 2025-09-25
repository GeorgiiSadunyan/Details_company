import pytest
from main import Supplier, SupplierMini

# обычный способ
s1 = Supplier(1, "АвтоДеталь", "+79991234567", "Москва")
print(s1)
print(repr(s1))

# Сравнение
s5 = Supplier(1, "АвтоДеталь", "+79991234567", "Москва")
print(s1 == s5)
print()


# Словарь JSON
data = {
    "supplier_id": 2,
    "name": "ЗапчастиПлюс",
    "phone": "+78887776655",
    "address": None
}
s2 = Supplier.from_dict(data)
print(s2)


# Строка
# С адресом
s3 = Supplier.from_csv_string("3,Автоцентр,Санкт-Петербург,+71234567890")
# Без адреса (3 поля)
s4 = Supplier.from_csv_string("4,МагазинЗапчастей,+70001112233")
print(s3)
print(s4)







# ============ Тесты для Supplier ============

def test_supplier_creation():
    s = Supplier(1, "АвтоДеталь", "+79991234567", "Москва")
    assert s.supplier_id == 1
    assert s.name == "АвтоДеталь"
    assert s.phone == "+79991234567"
    assert s.address == "Москва"

def test_supplier_without_address():
    s = Supplier(2, "ЗапчастиПлюс", "89876543210")
    assert s.address is None

def test_supplier_from_dict():
    data = {
        "supplier_id": 3,
        "name": "Тест",
        "phone": "+71234567890",
        "address": None
    }
    s = Supplier.from_dict(data)
    assert s.supplier_id == 3
    assert s.address is None

def test_supplier_from_csv_4_fields():
    s = Supplier.from_csv_string("4,Магазин,Санкт-Петербург,+71112223344")
    assert s.supplier_id == 4
    assert s.address == "Санкт-Петербург"

def test_supplier_from_csv_3_fields():
    s = Supplier.from_csv_string("5,Магазин,+71112223344")
    assert s.supplier_id == 5
    assert s.address is None

def test_supplier_to_mini():
    full = Supplier(6, "Полный", "+70000000000", "Город")
    mini = full.to_mini()
    assert isinstance(mini, SupplierMini)
    assert mini.supplier_id == 6
    assert mini.name == "Полный"

# ❌НАМЕРЕННАЯ ОШИБКА: телефон слишком короткий → вызовет ValueError
def test_supplier_eq():
    s1 = Supplier(7, "A", "+7111", "Addr")  # ← некорректный номер!
    s2 = Supplier(7, "A", "+7111", "Addr")
    assert s1 == s2  # никогда не выполнится — объекты не создаются


# ============ Тесты для SupplierMini ============

def test_supplier_mini_creation():
    m = SupplierMini(10, "Краткий")
    assert m.supplier_id == 10
    assert m.name == "Краткий"

# ❌НАМЕРЕННАЯ ОШИБКА: в словаре нет поля 'name'
def test_supplier_mini_from_dict():
    data = {"supplier_id": 11}  # ← нет 'name'!
    m = SupplierMini.from_dict(data)
    assert m.supplier_id == 11

# ❌НАМЕРЕННАЯ ОШИБКА: CSV с пустым именем
def test_supplier_mini_from_csv():
    m = SupplierMini.from_csv_string("12,")  # ← имя пустое → ошибка валидации
    assert m.supplier_id == 12

def test_supplier_mini_eq():
    m1 = SupplierMini(13, "X")
    m2 = SupplierMini(13, "X")
    assert m1 == m2


# ============ Тесты на вызов ошибок ============

def test_supplier_invalid_id():
    with pytest.raises(ValueError, match="положительным целым числом"):
        Supplier(-1, "Неверный ID", "+79991234567")

def test_supplier_mini_invalid_csv_format():
    with pytest.raises(ValueError, match="должна иметь id и наименование"):
        SupplierMini.from_csv_string("1")  # мало полей

def test_supplier_invalid_phone():
    with pytest.raises(ValueError, match="Некорректно набран номер"):
        Supplier(1, "Тест", "123")  # неверный телефон

def test_supplier_mini_invalid_id_in_csv():
    with pytest.raises(ValueError, match="id должен быть целым числом"):
        SupplierMini.from_csv_string("abc,Название")

# ❌НАМЕРЕННАЯ ОШИБКА: тест должен проверять ошибку, но НЕ использует pytest.raises
def test_supplier_missing_field_in_dict():
    # Этот тест УПАДЁТ, потому что мы НЕ ловим исключение
    Supplier.from_dict({"name": "Тест", "phone": "+7999"})  # ← нет supplier_id → ValueError!