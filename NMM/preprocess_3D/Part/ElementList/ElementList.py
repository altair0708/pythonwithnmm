from NMM.base.EntityList.EntityList import EntityList


class PreprocessElementList(EntityList):
    def __init__(self):
        super(PreprocessElementList, self).__init__()
        self._name = 'preprocess_element_list'
