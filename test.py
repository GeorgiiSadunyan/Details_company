from main import Supplier

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


