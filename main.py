from modules.Decorators import SupplierDB_Decorator, SupplierFiles_Decorator
from modules.supplier_rep_DB import Supplier_rep_DB
from modules.supplier_rep_yaml import Supplier_rep_yaml

repo = Supplier_rep_DB()
decorated_repo = SupplierDB_Decorator(repo)

# Пример: получить 1-ю "страницу" по 5 элементов,
# отсортированных по name, с фильтром по address
short_list = decorated_repo.get_k_n_short_list(
    k=1,
    n=5,
    filter_field="address",
    filter_value="г. Новороссийск, ул. Кубанская, д. 22",
    sort_field="supplier_id",
)

print("Список (отфильтрованный и отсортированный):")
for item in short_list:
    print(item)


count = decorated_repo.get_count(
    filter_field="address", filter_value="г. Новороссийск, ул. Кубанская, д. 22"
)
print(f"\nКоличество поставщиков с этим адресом: {count}")

repo.close()

print()
print()


file_repo = Supplier_rep_yaml("utils/DB/suppliers.yaml")
decorated_repo = SupplierFiles_Decorator(file_repo)

short_list2 = decorated_repo.get_k_n_short_list(
    k=1,
    n=10,
    filter_field="name",
    filter_value="КрасДонСтрой",
    sort_field="supplier_id",
)

count = decorated_repo.get_count(filter_field="name", filter_value="КрасДонСтрой")


print(count)

for item in short_list2:
    print(item)
