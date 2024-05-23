from abc import ABC, abstractmethod


class FactoryInterface:
    @abstractmethod
    def creat_an_element(self):
        pass
