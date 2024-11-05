from NMM.base.Algorithm.ElementCreator.MatrixElementCreator import MatrixElementCreator


class ElementCreatorFactory:
    @staticmethod
    def get_element_creator(element_type: str):
        if 'matrix_element' == element_type:
            return MatrixElementCreator()


