import psycopg2
from modules.supplier import Supplier
from modules.supplier_mini import SupplierMini
from modules.supplierDBconnection import SupplierDBConnection


class Supplier_rep_DB:
    def __init__(self):
        self.db = SupplierDBConnection()
            

    # a. Получить объект по ID
    def get_by_id(self, supplier_id: int) -> Supplier | None:
        query = "SELECT supplier_id, name, phone, address FROM suppliers WHERE supplier_id = %s;"
        result = self.db._execute_query(query, (supplier_id,))
        if result:
            row = result[0]
            return Supplier(
                name=row[1],
                phone=row[2],
                address=row[3],
                supplier_id=row[0]
            )
        return None
    

    # b. Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k: int, n: int) -> list[SupplierMini]:
        offset = (k - 1) * n
        query = """
        SELECT supplier_id, name FROM suppliers
        ORDER BY supplier_id
        LIMIT %s OFFSET %s;
        """
        result = self.db._execute_query(query, (n, offset))
        return [SupplierMini(supplier_id=row[0], name=row[1]) for row in result]
    

    # c. Добавить объект в список (с новым ID)
    def add(self, supplier: Supplier): 
        # Проверка уникальности
        query = "SELECT supplier_id FROM suppliers WHERE name = %s OR phone = %s;"
        result = self.db._execute_query(query, (supplier.name, supplier.phone))
        if result:
            raise ValueError(f"Поставщик с именем '{supplier.name}' и/или телефоном '{supplier.phone}' уже существует.")
        
        query = """
            INSERT INTO suppliers (name, phone, address)
            VALUES (%s, %s, %s)
            RETURNING supplier_id;
        """
        with self.db.conn.cursor() as cur:
            cur.execute(query, (supplier.name, supplier.phone, supplier.address))
            new_id = cur.fetchone()[0]
            supplier.supplier_id = new_id


    # d. Заменить элемент списка по ID
    def replace_by_id(self, supplier_id: int, supplier: Supplier):
        query = """
        UPDATE suppliers
        SET name = %s, phone = %s, address = %s
        WHERE supplier_id = %s;
        """
        self.db._execute_update(query, (supplier.name, supplier.phone, supplier.address, supplier_id))


    # e. Удалить элемент списка по ID
    def remove_by_id(self, supplier_id: int):
        query = "DELETE FROM suppliers WHERE supplier_id = %s;"
        self.db._execute_update(query, (supplier_id,))


    # f. Получить количество элементов
    def get_count(self) -> int:
        query = "SELECT COUNT(*) FROM suppliers;"
        result = self.db._execute_query(query)
        return result[0][0]
    
    
    def close(self):
        return self.db._close()