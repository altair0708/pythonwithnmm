from abc import ABC, abstractmethod


class AbstractCache(ABC):
    def __init__(self):
        self._cache_list = []

    @abstractmethod
    def add_item(self, *args):
        pass
