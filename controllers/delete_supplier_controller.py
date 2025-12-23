"""
Контроллер для удаления поставщика
Паттерн MVC - Controller
"""

from modules.supplier_rep_observable import SupplierRepObservable


class DeleteSupplierController:
    """
    Контроллер для удаления поставщика
    Отвечает за валидацию ID и удаление записи через репозиторий
    """

    def __init__(self, repository: SupplierRepObservable):
        """
        Инициализация контроллера

        Args:
            repository: Observable репозиторий для работы с данными
        """
        self.repository = repository

    def validate_and_delete_supplier(self, supplier_id: int) -> dict:
        """
        Валидация и удаление поставщика

        Args:
            supplier_id: ID поставщика для удаления

        Returns:
            dict: Результат операции
                {
                    "success": bool,
                    "message": str,
                    "error": str (если ошибка)
                }
        """
        try:
            # Валидация ID
            if not isinstance(supplier_id, int) or supplier_id <= 0:
                return {"success": False, "error": "Некорректный ID поставщика"}

            # Проверка существования поставщика
            try:
                existing_supplier = self.repository.get_by_id(supplier_id)
                if existing_supplier is None:
                    return {
                        "success": False,
                        "error": f"Поставщик с ID {supplier_id} не найден",
                    }
            except Exception:
                return {
                    "success": False,
                    "error": f"Поставщик с ID {supplier_id} не найден",
                }

            # Удаление через Observable (который уведомит Observer'ов)
            self.repository.remove_by_id(supplier_id)

            return {
                "success": True,
                "message": f"Поставщик '{existing_supplier.name}' успешно удален",
                "supplier_id": supplier_id,
            }

        except ValueError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка при удалении поставщика: {str(e)}",
            }
