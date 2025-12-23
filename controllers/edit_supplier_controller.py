"""
Контроллер для редактирования поставщика
Отдельный контроллер согласно паттерну MVC для окна редактирования
"""

from modules.supplier import Supplier
from modules.supplier_rep_observable import SupplierRepObservable


class EditSupplierController:
    """
    Контроллер для окна редактирования поставщика
    Отвечает за получение данных, валидацию и обновление поставщика
    """

    def __init__(self, repository: SupplierRepObservable):
        self.repository = repository

    def get_supplier_for_edit(self, supplier_id: int) -> dict:
        """
        Получить данные поставщика для редактирования

        Args:
            supplier_id: ID поставщика

        Returns:
            Словарь с данными поставщика или ошибкой
        """
        try:
            supplier = self.repository.get_by_id(supplier_id)

            if supplier is None:
                return {
                    "success": False,
                    "error": f"Поставщик с ID {supplier_id} не найден"
                }

            return {
                "success": True,
                "supplier": {
                    "supplier_id": supplier.supplier_id,
                    "name": supplier.name,
                    "phone": supplier.phone,
                    "address": supplier.address
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка при получении данных: {str(e)}"
            }

    def validate_and_update_supplier(
        self, supplier_id: int, name: str, phone: str, address: str = None  # type: ignore
    ) -> dict:
        """
        Валидация и обновление данных поставщика

        Args:
            supplier_id: ID поставщика
            name: новое название
            phone: новый телефон
            address: новый адрес (опционально)

        Returns:
            Результат операции с детальной информацией об ошибках
        """
        # Проверка существования поставщика
        existing_supplier = self.repository.get_by_id(supplier_id)
        if existing_supplier is None:
            return {
                "success": False,
                "error": f"Поставщик с ID {supplier_id} не найден",
                "validation_errors": {"general": "Поставщик не существует"}
            }

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
            supplier = Supplier(
                name=name.strip(),
                phone=phone.strip(),
                address=address.strip() if address else None
            )
            supplier.supplier_id = supplier_id # Устанавливаем ID редактируемого п-ка
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

        # Попытка обновления в репозитории
        try:
            self.repository.replace_by_id(supplier_id, supplier)
            return {
                "success": True,
                "message": "Поставщик успешно обновлен",
                "supplier_id": supplier_id,
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "validation_errors": {"general": str(e)},
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка при обновлении поставщика: {str(e)}",
                "validation_errors": {"general": str(e)},
            }

