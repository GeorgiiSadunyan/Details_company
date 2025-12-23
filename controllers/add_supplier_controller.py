"""
Контроллер для добавления нового поставщика
Отдельный контроллер согласно паттерну MVC для нового окна
"""

from modules.supplier import Supplier
from modules.supplier_rep_observable import SupplierRepObservable


class AddSupplierController:
    """
    Контроллер для окна добавления поставщика
    Отвечает за валидацию и добавление нового поставщика
    """

    def __init__(self, repository: SupplierRepObservable):
        self.repository = repository

    def validate_and_add_supplier(
        self, name: str, phone: str, address: str = None  # type: ignore
    ) -> dict:
        """
        Валидация и добавление нового поставщика

        Args:
            name: название поставщика
            phone: телефон
            address: адрес (опционально)

        Returns:
            Результат операции с детальной информацией об ошибках
        """
        # Словарь для сбора ошибок валидации
        validation_errors = {}

        # Проверка обязательных полей
        if not name or not name.strip():
            validation_errors["name"] = "Поле 'Наименование' обязательно для заполнения"

        if not phone or not phone.strip():
            validation_errors["phone"] = "Поле 'Телефон' обязательно для заполнения"

        # Если есть ошибки в обязательных полях, возвращаем их
        if validation_errors:
            return {
                "success": False,
                "error": "Ошибка валидации данных",
                "validation_errors": validation_errors,
            }

        # Попытка создания объекта поставщика (здесь произойдет валидация формата)
        try:
            supplier = Supplier(name=name.strip(), phone=phone.strip(), address=address.strip() if address else None)
        except ValueError as e:
            # Парсим ошибку и определяем поле
            error_msg = str(e)
            if "телефон" in error_msg.lower() or "phone" in error_msg.lower():
                validation_errors["phone"] = error_msg
            elif "имя" in error_msg.lower() or "name" in error_msg.lower():
                validation_errors["name"] = error_msg
            elif "адрес" in error_msg.lower() or "address" in error_msg.lower():
                validation_errors["address"] = error_msg
            else:
                validation_errors["general"] = error_msg

            return {
                "success": False,
                "error": "Ошибка валидации данных",
                "validation_errors": validation_errors,
            }

        # Попытка добавления в репозиторий
        try:
            self.repository.add(supplier)
            return {
                "success": True,
                "message": "Поставщик успешно добавлен",
                "supplier_id": supplier.supplier_id,
            }
        except ValueError as e:
            # Ошибка уникальности
            return {
                "success": False,
                "error": str(e),
                "validation_errors": {"general": str(e)},
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка при добавлении поставщика: {str(e)}",
                "validation_errors": {"general": str(e)},
            }

