from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure
from NMM.base.Object.Builder.ConstructorInterface import AbstractConstructor
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class DataStructureBuilder(AbstractConstructor):
    def build(self):
        data_structure = DataStructure()

        return data_structure
