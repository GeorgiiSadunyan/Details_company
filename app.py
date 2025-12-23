"""
Веб-приложение для управления поставщиками
Архитектура: MVC (Model-View-Controller)
Паттерн: Observer для уведомления об изменениях данных

Без использования веб-фреймворков (используется только встроенный http.server)
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from controllers.add_supplier_controller import AddSupplierController
from controllers.edit_supplier_controller import EditSupplierController
from controllers.supplier_controller import SupplierController
from modules.observer import Observer
from modules.supplier_rep_DB import Supplier_rep_DB
from modules.supplier_rep_observable import SupplierRepObservable


class ViewObserver(Observer):
    """
    Наблюдатель для View - реализация паттерна Observer
    Получает уведомления об изменениях данных от Subject (репозитория)
    """

    def __init__(self):
        self.events = []

    def update(self, event_type: str, data=None):
        """Получение уведомления об изменении"""
        event_info = {"event_type": event_type, "data": str(data) if data else None}
        self.events.append(event_info)
        print(f"[Observer] Получено событие: {event_type}")
        if data:
            print(f"[Observer] Данные: {data}")


class SupplierRequestHandler(BaseHTTPRequestHandler):
    """
    Обработчик HTTP запросов
    Маршрутизация запросов к соответствующим методам контроллера
    """

    # Статические переменные для контроллеров
    controller: SupplierController = None  # type: ignore
    add_controller: AddSupplierController = None  # type: ignore
    edit_controller: EditSupplierController = None  # type: ignore
    view_observer: ViewObserver = None  # type: ignore

    def do_GET(self):
        """Обработка GET запросов"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # Маршрутизация
        if path == "/":
            self.serve_html("views/index.html")
        elif path == "/add_supplier":
            self.serve_html("views/add_supplier.html")
        elif path == "/edit_supplier":
            self.serve_html("views/edit_supplier.html")
        elif path.startswith("/static/"):
            self.serve_static(path)
        elif path == "/api/suppliers":
            self.get_suppliers_list(query_params)
        elif path.startswith("/api/suppliers/"):
            supplier_id = path.split("/")[-1]
            if supplier_id.isdigit():
                self.get_supplier_details(int(supplier_id))
            else:
                self.send_error_response(400, "Некорректный ID поставщика")
        else:
            self.send_error_response(404, "Страница не найдена")

    def get_suppliers_list(self, query_params):
        """Получить список поставщиков (краткая информация)"""
        try:
            page = int(query_params.get("page", ["1"])[0])
            page_size = int(query_params.get("page_size", ["10"])[0])

            # Вызов метода контроллера
            result = self.controller.get_suppliers_page(page, page_size)
            self.send_json_response(result)
        except ValueError as e:
            self.send_error_response(400, str(e))
        except Exception as e:
            self.send_error_response(500, f"Внутренняя ошибка сервера: {str(e)}")

    def get_supplier_details(self, supplier_id: int):
        """Получить полную информацию о поставщике"""
        try:
            # Вызов метода контроллера
            result = self.controller.get_supplier_details(supplier_id)
            self.send_json_response(result)
        except Exception as e:
            self.send_error_response(500, f"Внутренняя ошибка сервера: {str(e)}")

    def serve_html(self, filepath):
        """Отдать HTML файл"""
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error_response(404, "Файл не найден")

    def serve_static(self, path):
        """Отдать статические файлы (CSS, JS)"""
        # Убираем /static/ и добавляем views/static/
        filename = path.replace("/static/", "")
        filepath = f"views/static/{filename}"

        try:
            # Определяем MIME-тип
            if filepath.endswith(".css"):
                content_type = "text/css"
            elif filepath.endswith(".js"):
                content_type = "application/javascript"
            else:
                content_type = "text/plain"

            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", f"{content_type}; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error_response(404, f"Файл не найден: {filepath}")

    def send_json_response(self, data):
        """Отправить JSON ответ"""
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        json_data = json.dumps(data, ensure_ascii=False)
        self.wfile.write(json_data.encode("utf-8"))

    def send_error_response(self, code, message):
        """Отправить ответ с ошибкой"""
        self.send_response(code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        error_data = {"success": False, "error": message}
        json_data = json.dumps(error_data, ensure_ascii=False)
        self.wfile.write(json_data.encode("utf-8"))

    def do_POST(self):
        """Обработка POST запросов"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Маршрутизация POST запросов
        if path == "/api/suppliers/add":
            self.add_supplier()
        else:
            self.send_error_response(404, "Endpoint не найден")

    def do_PUT(self):
        """Обработка PUT запросов"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Маршрутизация PUT запросов
        if path == "/api/suppliers/edit":
            self.edit_supplier()
        else:
            self.send_error_response(404, "Endpoint не найден")

    def add_supplier(self):
        """Добавление нового поставщика через AddSupplierController"""
        try:
            # Читаем данные из тела запроса
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            # Извлекаем параметры
            name = data.get("name", "")
            phone = data.get("phone", "")
            address = data.get("address")

            # Вызываем метод контроллера добавления
            result = self.add_controller.validate_and_add_supplier(name, phone, address)
            self.send_json_response(result)
        except json.JSONDecodeError:
            self.send_error_response(400, "Некорректный JSON")
        except Exception as e:
            self.send_error_response(500, f"Внутренняя ошибка сервера: {str(e)}")

    def edit_supplier(self):
        """Редактирование поставщика через EditSupplierController"""
        try:
            # Читаем данные из тела запроса
            content_length = int(self.headers.get("Content-Length", 0))
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode("utf-8"))

            # Извлекаем параметры
            supplier_id = data.get("supplier_id")
            name = data.get("name", "")
            phone = data.get("phone", "")
            address = data.get("address")

            if not supplier_id:
                self.send_error_response(400, "Не указан ID поставщика")
                return

            # Вызываем метод контроллера редактирования
            result = self.edit_controller.validate_and_update_supplier(
                supplier_id, name, phone, address
            )
            self.send_json_response(result)
        except json.JSONDecodeError:
            self.send_error_response(400, "Некорректный JSON")
        except Exception as e:
            self.send_error_response(500, f"Внутренняя ошибка сервера: {str(e)}")

    def log_message(self, format, *args):
        """Переопределение логирования для более читаемого вывода"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def initialize_app():
    """
    Инициализация приложения
    Создание репозитория, наблюдателя, контроллера
    """
    print("=" * 60)
    print("Инициализация приложения...")
    print("=" * 60)

    # Создаем репозиторий
    base_repository = Supplier_rep_DB()
    print("[OK] БД инициализирована")

    # Оборачиваем в Observable (Subject)
    observable_repo = SupplierRepObservable(base_repository)
    print("[OK] Observable репозиторий создан (паттерн Observer)")

    # Создаем наблюдателя для View
    view_observer = ViewObserver()
    observable_repo.attach(view_observer)
    print("[OK] View Observer подписан на изменения данных")

    # Создаем контроллеры
    controller = SupplierController(observable_repo)
    print("[OK] Главный контроллер создан (паттерн MVC)")

    add_controller = AddSupplierController(observable_repo)
    print("[OK] Контроллер добавления создан (паттерн MVC для нового окна)")

    edit_controller = EditSupplierController(observable_repo)
    print("[OK] Контроллер редактирования создан (паттерн MVC для нового окна)")

    print("=" * 60)
    print("[OK] Приложение успешно инициализировано!")
    print("=" * 60)
    print()

    return controller, add_controller, edit_controller, view_observer


def run_server(host="localhost", port=8000):
    """
    Запуск HTTP сервера
    """
    # Инициализация приложения
    controller, add_controller, edit_controller, view_observer = initialize_app()

    # Устанавливаем контроллеры для обработчика запросов
    SupplierRequestHandler.controller = controller
    SupplierRequestHandler.add_controller = add_controller
    SupplierRequestHandler.edit_controller = edit_controller
    SupplierRequestHandler.view_observer = view_observer

    # Создаем и запускаем сервер
    server = HTTPServer((host, port), SupplierRequestHandler)

    print(f">>> Сервер запущен на {host}:{port}")
    print(f">>> Откройте браузер и перейдите по адресу: http://{host}:{port}/")
    print(">>> Для остановки сервера нажмите Ctrl+C")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print(">>> Сервер остановлен")
        print("=" * 60)
        server.shutdown()


if __name__ == "__main__":
    run_server()
