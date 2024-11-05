from NMM.base.EntityList.EntityList import EntityList


class ElementList(EntityList):
    def __init__(self, element_type: str):
        super(ElementList, self).__init__()
        self.name = element_type

    def add_element(self, new_element_list):
        pass
