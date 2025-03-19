from abc import ABC, abstractmethod


class AbstractElementBuilder(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_element(self):
        pass
