"""
Модуль содержит базовые классы моделей предметной области.
"""

from .detail import Detail
from .detail_base import DetailBase
from .detail_mini import DetailMini
from .supplier import Supplier
from .supplier_base import SupplierBase
from .supplier_mini import SupplierMini

__all__ = [
    "SupplierBase",
    "Supplier",
    "SupplierMini",
    "DetailBase",
    "Detail",
    "DetailMini",
]
