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

    # interface in VtkGrid, DatabaseTable
    def insert(self):
        for each_observer in self._inform_list:
            each_observer.insert(self._cache_list[-1])

    # interface in DatabaseTable
    def select(self):
        result_list = []
        for each_observer in self._inform_list:
            each_observer.select(self._cache_list[-1], result_list)
        return result_list

    @abstractmethod
    def add_item(self, *args):
        pass

    def get_item(self, *args):
        pass
