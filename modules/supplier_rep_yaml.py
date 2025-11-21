from modules.supplier_rep_base import supplier_rep_base
from typing import Any
import yaml


class Supplier_rep_yaml(supplier_rep_base):
    
    '''Класс для работы с YAML'''
    
    def load(self, file) -> list[dict[str, Any]]:
        content = file.read()
        if content.strip():
            return yaml.safe_load(content)
        return []
    
    def save(self, file):
        yaml.dump(self.data, file, allow_unicode=True)