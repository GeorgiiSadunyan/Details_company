"""
Контроллер для управления поставщиками
Вся бизнес-логика вынесена сюда - НЕТ логики в классах View
"""

from modules.models.supplier import Supplier
from modules.repositories import SupplierRepObservable


class SupplierController:
    """
    Контроллер для главной страницы со списком поставщиков
    Отвечает за обработку запросов и взаимодействие с моделью
    """

    def __init__(self, repository: SupplierRepObservable):
        self.repository = repository

    def get_suppliers_page(
        self,
        page: int = 1,
        page_size: int = 10,
        filter_field: str = None,  # type: ignore
        filter_value: str = None,  # type: ignore
        sort_field: str = "supplier_id",
    ) -> dict:
        """
        Получить страницу со списком поставщиков (краткая информация)
        С поддержкой фильтрации и сортировки через Decorator Pattern

        Args:
            page: номер страницы (начиная с 1)
            page_size: количество элементов на странице
            filter_field: поле для фильтрации (name, phone, address)
            filter_value: значение для фильтрации
            sort_field: поле для сортировки (supplier_id, name, phone, address)

        Returns:
            Словарь с данными: items, total_count, page, page_size, total_pages
        """
        try:
            # Используем Decorator Pattern для фильтрации и сортировки
            from modules.Decorators import SupplierDB_Decorator
            from modules.repositories import Supplier_rep_DB

            # Получаем базовый репозиторий из Observable
            base_repo = self.repository.repository

            # Если это DB репозиторий, используем декоратор
            if isinstance(base_repo, Supplier_rep_DB):
                decorator = SupplierDB_Decorator(base_repo)

                # Получаем краткий список с фильтрацией и сортировкой
                suppliers_mini = decorator.get_k_n_short_list(
                    k=page,
                    n=page_size,
                    filter_field=filter_field,
                    filter_value=filter_value,
                    sort_field=sort_field,
                )

                # Получаем общее количество с учетом фильтра
                total_count = decorator.get_count(
                    filter_field=filter_field, filter_value=filter_value
                )
            else:
                # Для файловых репозиториев используем файловый декоратор
                from modules.Decorators import SupplierFiles_Decorator

                decorator = SupplierFiles_Decorator(base_repo)

                suppliers_mini = decorator.get_k_n_short_list(
                    k=page,
                    n=page_size,
                    filter_field=filter_field,
                    filter_value=filter_value,
                    sort_field=sort_field,
                )

                total_count = decorator.get_count(
                    filter_field=filter_field, filter_value=filter_value
                )

            # Вычисляем общее количество страниц
            if total_count > 0:
                total_pages = (total_count + page_size - 1) // page_size
            else:
                total_pages = 1

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

    def add_supplier(self, name: str, phone: str, address: str = None) -> dict:  # type: ignore
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

    def update_supplier(
        self,
        supplier_id: int,
        name: str,
        phone: str,
        address: str = None,  # type: ignore
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
