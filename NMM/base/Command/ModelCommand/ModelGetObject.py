from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache


class ModelGetObject(AbstractCommand):
    def __init__(self, object_name):
        self.__object_name = object_name

    def execute(self):
        return entrance_cache.get_item(self.__object_name)

