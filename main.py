from modules.supplier_mini import SupplierMini
from modules.supplier import Supplier
from modules.supplier_rep_json import Supplier_rep_json
from modules.supplier_rep_yaml import Supplier_rep_yaml

def main():
    
    # repo = Supplier_rep_json('utils/DB/suppliers.json')
    repo = Supplier_rep_yaml('utils/DB/suppliers.yaml')


    supplier_dict = {
        'supplier_id': 0,
        'name': 'КрасДонСтрой',
        'address': 'Селезнёва 2',
        'phone': '+79993338844'
    }

    supplier1 = Supplier(supplier_dict)
    repo.add(supplier1)

    # Получаем все
    all_suppliers = repo.get_all()
    for supplier in all_suppliers:
        print(supplier)
    
    # Получаем по ID
    found = repo.get_by_id(1)
    print(found)

    # Сортировка
    repo.sort_by_field('name')

    # Количество
    count = repo.get_count()
    print(count)
    
    
    supplier2 = Supplier(supplier_id=0, name="КрасСтрой", phone="+71234578777", address="ГородКраснодар")
    repo.replace_by_id(1, supplier2)    


    all_suppliers = repo.get_all()
    for supplier in all_suppliers:
        print(supplier)



if __name__ == "__main__":
    main()