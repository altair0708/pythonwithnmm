from abc import ABC, abstractmethod


class AbstractCache(ABC):
    def __init__(self):
        self._cache_list = []
        self._inform_list = []

    def __len__(self):
        return len(self._cache_list)

    def __iter__(self):
        return iter(self._cache_list)

    def add_observer(self, observer):
        self._inform_list.append(observer)

    def remove_observer(self, observer):
        self._inform_list.remove(observer)

    def update(self):
        for each_observer in self._inform_list:
            each_observer.modify(self._cache_list[-1])

    @abstractmethod
    def add_item(self, *args):
        pass
