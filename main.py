from modules.supplier import Supplier
from modules.supplier_rep_json import Supplier_rep_json
from modules.supplier_rep_yaml import Supplier_rep_yaml
from modules.supplier_rep_DB import Supplier_rep_DB
from modules.Decorators import SupplierDB_FilterSort_Decorator


repo = Supplier_rep_DB()
decorated_repo = SupplierDB_FilterSort_Decorator(repo)

# Пример: получить 1-ю "страницу" по 5 элементов, отсортированных по name, с фильтром по address
short_list = decorated_repo.get_k_n_short_list(
    k=1,
    n=5,
    filter_field='address',
    filter_value='г. Новороссийск, ул. Кубанская, д. 22',
    sort_field='supplier_id'
)

print("Список (отфильтрованный и отсортированный):")
for item in short_list:
    print(item)


count = decorated_repo.get_count(filter_field='address', filter_value='г. Новороссийск, ул. Кубанская, д. 22')
print(f"\nКоличество поставщиков с этим адресом: {count}")

repo.close()