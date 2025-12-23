import json
from typing import Any

from modules.repositories.supplier_rep_base import supplier_rep_base


class Supplier_rep_json(supplier_rep_base):
    """Класс для работы с JSON"""

    def load(self, file) -> list[dict[str, Any]]:
        content = file.read()
        if content.strip():
            return json.loads(content)
        return []

    def save(self, file):
        json.dump(self.data, file, ensure_ascii=False, indent=2)
