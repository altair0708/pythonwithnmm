from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase import entrance_cache
from NMM.base.Algorithm.ElementCreator.ElementCreatorFactory import ElementCreatorFactory
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.preprocess_3D.Part.ElementList.ElementList import ElementList


class ModelGenerateElementList(AbstractCommand):
    def __init__(self, element_type: str):
        self.__element_list: ElementList = entrance_cache.get_item(f'{element_type}_list_Part')
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')

        self.__element_creator = ElementCreatorFactory.get_element_creator(element_type)

    def execute(self):
        for each_id in range(self.__manifold_element.get_number()):
            self.__element_creator.set_input_data(each_id, self.__manifold_element, self.__new_element)
            self.__element_list.add_element(self.__element_creator.update())
