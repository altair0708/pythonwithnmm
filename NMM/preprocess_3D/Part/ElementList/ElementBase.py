from NMM.preprocess_3D.Part.ElementList.MatrixElement.ElementInterface import AbstractElement


class ElementBase(AbstractElement):
    def __init__(self, name):
        super().__init__()
        self.name = name
