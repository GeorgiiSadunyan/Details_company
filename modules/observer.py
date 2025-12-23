"""
Паттерн Observer для уведомления об изменениях в данных
"""

from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    """Абстрактный класс наблюдателя"""

    @abstractmethod
    def update(self, event_type: str, data: Any = None):
        """
        Метод, вызываемый при изменении состояния Subject

        Args:
            event_type: тип события (data_loaded, data_updated и т.д.)
            data: данные события
        """
        pass


class Subject(ABC):
    """Абстрактный класс наблюдаемого объекта (Subject)"""

    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        """Подписать наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Отписать наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: str, data: Any = None):
        """Уведомить всех наблюдателей об изменении"""
        for observer in self._observers:
            observer.update(event_type, data)
