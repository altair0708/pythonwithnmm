from NMM.base.Object.Builder.Object import Object
from abc import ABC


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class Model(Object, ABC):
    pass

