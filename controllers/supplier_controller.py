"""
Контроллер для управления поставщиками
Вся бизнес-логика вынесена сюда - НЕТ логики в классах View
"""

from modules.supplier import Supplier
from modules.supplier_rep_observable import SupplierRepObservable


class SupplierController:
    """
    Контроллер для главной страницы со списком поставщиков
    Отвечает за обработку запросов и взаимодействие с моделью
    """

    def __init__(self, repository: SupplierRepObservable):
        self.repository = repository

    def get_suppliers_page(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Получить страницу со списком поставщиков (краткая информация)

        Args:
            page: номер страницы (начиная с 1)
            page_size: количество элементов на странице

        Returns:
            Словарь с данными: items, total_count, page, page_size, total_pages
        """
        try:
            # Получаем краткий список поставщиков
            suppliers_mini = self.repository.get_k_n_short_list(page, page_size)

            # Получаем общее количество
            total_count = self.repository.get_count()

            # Вычисляем общее количество страниц
            total_pages = (total_count + page_size - 1) // page_size

            return {
                "success": True,
                "items": [
                    {"supplier_id": s.supplier_id, "name": s.name}
                    for s in suppliers_mini
                ],
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_supplier_details(self, supplier_id: int) -> dict:
        """
        Получить полную информацию о поставщике по ID

        Args:
            supplier_id: ID поставщика

        Returns:
            Словарь с полными данными поставщика
        """
        try:
            supplier = self.repository.get_by_id(supplier_id)

            if supplier is None:
                return {
                    "success": False,
                    "error": f"Поставщик с ID {supplier_id} не найден",
                }

            return {
                "success": True,
                "supplier": {
                    "supplier_id": supplier.supplier_id,
                    "name": supplier.name,
                    "phone": supplier.phone,
                    "address": supplier.address,
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_supplier(self,
                     name: str,
                     phone: str,
                     address: str = None) -> dict: # type: ignore
        """
        Добавить нового поставщика

        Args:
            name: название поставщика
            phone: телефон
            address: адрес (опционально)

        Returns:
            Результат операции
        """
        try:
            supplier = Supplier(name=name, phone=phone, address=address)
            self.repository.add(supplier)
            return {
                "success": True,
                "message": "Поставщик успешно добавлен",
                "supplier_id": supplier.supplier_id,
            }
        except ValueError as e:
            return {"success": False, "error": f"Ошибка валидации: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_supplier(self,
                        supplier_id: int,
                        name: str,
                        phone: str,
                        address: str = None # type: ignore
    ) -> dict:
        """
        Обновить данные поставщика

        Args:
            supplier_id: ID поставщика
            name: название поставщика
            phone: телефон
            address: адрес (опционально)

        Returns:
            Результат операции (словарь)
        """
        try:
            supplier = Supplier(name=name, phone=phone, address=address)
            self.repository.replace_by_id(supplier_id, supplier)
            return {"success": True, "message": "Поставщик успешно обновлён"}
        except ValueError as e:
            return {"success": False, "error": f"Ошибка валидации: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_supplier(self, supplier_id: int) -> dict:
        """
        Удалить поставщика

        Args:
            supplier_id: ID поставщика

        Returns:
            Результат операции
        """
        try:
            self.repository.remove_by_id(supplier_id)
            return {"success": True, "message": "Поставщик успешно удалён"}
        except Exception as e:
            return {"success": False, "error": str(e)}
