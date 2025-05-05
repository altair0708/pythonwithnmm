from NMM.base.Property.Property import Property
from numpy.linalg.linalg import eigh
import numpy as np


class PropertyTensor(Property):
    def __init__(self, value=None):
        super(PropertyTensor, self).__init__()
        self._type = 'PropertyTensor'
        self._name = ''
        self._value = value

        if value is not None:
            assert value.shape == (6, 1)
            self.__tensor_total = value
        else:
            self.__tensor_total = np.array([[0], [0], [0], [0], [0], [0]])

        # sigma(x) sigma(y) sigma(z) tau(xy) tau(xz) tau(yz)
        self.__xx = self.__tensor_total[0, 0]
        self.__yy = self.__tensor_total[1, 0]
        self.__zz = self.__tensor_total[2, 0]
        self.__xy = self.__tensor_total[3, 0]
        self.__yz = self.__tensor_total[4, 0]
        self.__xz = self.__tensor_total[5, 0]

        self.__matrix = np.matrix([[self.__xx, self.__xy, self.__xz],
                                   [self.__xy, self.__yy, self.__yz],
                                   [self.__xz, self.__yz, self.__zz]], dtype=np.float64)

        self.__eigenvalue_vector, self.__eigenvector_matrix = eigh(self.__matrix)

        # self.__component_1 = [self.__eigenvalue_vector[0], self.__eigenvector_matrix[0]]
        # self.__component_2 = [self.__eigenvalue_vector[1], self.__eigenvector_matrix[1]]
        # self.__component_3 = [self.__eigenvalue_vector[2], self.__eigenvector_matrix[2]]
        self.__component_1 = [self.__eigenvalue_vector[0], self.__eigenvector_matrix[:, 0].reshape((1, 3))]
        self.__component_2 = [self.__eigenvalue_vector[1], self.__eigenvector_matrix[:, 1].reshape((1, 3))]
        self.__component_3 = [self.__eigenvalue_vector[2], self.__eigenvector_matrix[:, 2].reshape((1, 3))]

        def max_component(component_1, component_2):
            if component_1[0] > component_2[0]:
                return component_1
            else:
                return component_2

        self.__max_component = max_component(self.__component_1, self.__component_2)
        self.__max_component = max_component(self.__max_component, self.__component_3)

        # sort
        self.__component_list = [self.__component_1, self.__component_2, self.__component_3]
        self.__component_list.sort(key=lambda a: a[0])
        self.__min_component = self.__component_list[0]
        self.__middle_component = self.__component_list[1]

        assert self.__max_component == self.__component_list[2]

    @property
    def max_component_vector(self):
        return self.__max_component

    @property
    def middle_component_vector(self):
        return self.__middle_component

    @property
    def min_component_vector(self):
        return self.__min_component

    @property
    def component_vector_1(self):
        return self.__component_1

    @property
    def component_vector_2(self):
        return self.__component_2

    @property
    def component_vector_3(self):
        return self.__component_3
