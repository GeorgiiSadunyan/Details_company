"""
Модуль repositories содержит классы репозиториев для работы с данными.

Репозитории реализуют паттерны:
- Adapter (supplier_rep_DB)
- Observer (supplier_rep_observable)
- Decorator (через Decorators.py)
"""

from .supplier_rep_base import supplier_rep_base
from .supplier_rep_json import Supplier_rep_json
from .supplier_rep_yaml import Supplier_rep_yaml
from .supplier_rep_DB import Supplier_rep_DB
from .supplier_rep_observable import SupplierRepObservable

__all__ = [
    "supplier_rep_base",
    "Supplier_rep_json",
    "Supplier_rep_yaml",
    "Supplier_rep_DB",
    "SupplierRepObservable",
]

