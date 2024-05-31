from NMM.base.Part.DataStructure.DataStructure import DataStructure
from NMM.base.Object.Builder.ConstructorInterface import AbstractConstructor


class DataStructureBuilder(AbstractConstructor):
    def build(self):
        data_structure = DataStructure()

        return data_structure
