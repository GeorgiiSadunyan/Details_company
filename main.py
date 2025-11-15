from models.supplier_mini import SupplierMini
from models.supplier import Supplier
from utils.JSON.supplier_rep_json import Supplier_rep_json

def main():
    # Создаём репозиторий
    repo = Supplier_rep_json('utils/JSON/suppliers.json')

    # Добавляем поставщика
    s = Supplier(supplier_id=0, name="Новый", phone="+71234567890", address="Город")
    repo.add(s)

    # Получаем все
    all_suppliers = repo.get_all()
    print(all_suppliers)
    
    # Получаем по ID
    found = repo.get_by_id(1)
    print(found)

    # Сортировка
    repo.sort_by_field('name')

    
    # Количество
    count = repo.get_count()
    print(count)
    
    s2 = Supplier(supplier_id=0, name="КрасСтрой", phone="+71234578777", address="ГородКраснодар")
    repo.replace_by_id(1, s2)
    


if __name__ == "__main__":
    main()