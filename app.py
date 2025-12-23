from flask import Flask, jsonify, render_template, request

from controllers.add_supplier_controller import AddSupplierController
from controllers.delete_supplier_controller import DeleteSupplierController
from controllers.edit_supplier_controller import EditSupplierController
from controllers.supplier_controller import SupplierController
from modules.observer import Observer
from modules.repositories import Supplier_rep_DB, SupplierRepObservable


class ViewObserver(Observer):
    """
    Наблюдатель для View.
    """

    def update(self, event_type: str, data=None):
        print(f"[Observer] Событие: {event_type} | Данные: {data}")


# Настройка Flask
app = Flask(__name__, template_folder="views", static_folder="views/static")

# Глобальные переменные для контроллеров
controllers = {}


def initialize_app():
    """Инициализация архитектуры MVC + Observer"""
    print("=" * 60)
    print("Инициализация приложения (Flask)...")

    # 1. Model (Repository + Observer)
    base_repository = Supplier_rep_DB()
    observable_repo = SupplierRepObservable(base_repository)

    view_observer = ViewObserver()
    observable_repo.attach(view_observer)

    # 2. Controllers
    controllers["main"] = SupplierController(observable_repo)
    controllers["add"] = AddSupplierController(observable_repo)
    controllers["edit"] = EditSupplierController(observable_repo)
    controllers["delete"] = DeleteSupplierController(observable_repo)

    print("[OK] Архитектура загружена")
    print("=" * 60)


# ==========================================
# Маршруты (Routes) - Это View Layer
# ==========================================


@app.route("/")
def index():
    """Главная страница"""
    return render_template("index.html")


@app.route("/supplier_form")
def supplier_form():
    """Форма поставщика"""
    return render_template("supplier_form.html")


# ==========================================
# API Методы
# ==========================================


@app.route("/api/suppliers", methods=["GET"])
def get_suppliers_list():
    """Получить список поставщиков"""
    try:
        # Получение параметров из query string
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 10, type=int)
        filter_field = request.args.get("filter_field")
        filter_value = request.args.get("filter_value")
        sort_field = request.args.get("sort_field", "supplier_id")

        result = controllers["main"].get_suppliers_page(
            page=page,
            page_size=page_size,
            filter_field=filter_field,
            filter_value=filter_value,
            sort_field=sort_field,
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Internal Error: {str(e)}"}), 500


@app.route("/api/suppliers/<int:supplier_id>", methods=["GET"])
def get_supplier_details(supplier_id):
    """Получить одного поставщика"""
    try:
        result = controllers["main"].get_supplier_details(supplier_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/suppliers/add", methods=["POST"])
def add_supplier():
    """Добавление поставщика"""
    try:
        data = request.json  # Автоматический парсинг JSON
        if not data:
            return jsonify({"success": False, "error": "No JSON data"}), 400

        result = controllers["add"].validate_and_add_supplier(
            data.get("name", ""), data.get("phone", ""), data.get("address")
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route(
    "/api/suppliers/edit", methods=["PUT"]
)  # Можно также использовать POST или PATCH
def edit_supplier():
    """Редактирование поставщика"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "error": "No JSON data"}), 400

        supplier_id = data.get("supplier_id")
        if not supplier_id:
            return jsonify({"success": False, "error": "Missing supplier_id"}), 400

        result = controllers["edit"].validate_and_update_supplier(
            supplier_id,
            data.get("name", ""),
            data.get("phone", ""),
            data.get("address"),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/suppliers/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    """Удаление поставщика"""
    try:
        result = controllers["delete"].validate_and_delete_supplier(supplier_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # Инициализация перед запуском
    initialize_app()
    print(">>> Сервер запущен на http://localhost:8000")
    # debug=True позволяет серверу перезагружаться при изменении кода
    app.run(host="localhost", port=8000, debug=True)
