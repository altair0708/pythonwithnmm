from NMM.base.ObjectBase import NmmObjectBase


class CONST:
    DYNAMIC_COEFFICIENT = 1
    STEP = 0
    MATERIAL_TYPE = 1
    JOINT_TYPE = 1
    DISPLACEMENT_ALLOW = 0.003
    TIME_INCREMENT = 0.02
    CONSTANT_SPRING_STIFF = 1000000000000
    SOR_FACTOR = 1.80
    COORDINATE_SYSTEM = (0, 0, 0)
    TOLERANCE = 0.00001


class PATH:
    work_path = '../data_3D/'
    mesh_file = '../data_3D/mesh/'
    geometry_file = '../data_3D/geometry/'

    element_file = '../data_3D/geometry/manifold_element.vtu'
    mathcover_file = '../data_3D/geometry/math_cover.vtu'
    crack_file = '../data_3D/geometry/crack_surface.vtu'
    database_name = '../data_3D/geometry/manifold_mathcover.db'
    special_point_file = '../data_3D/mesh/special_point.vtu'
    material_coefficient_file = '../data_3D/materical/material_coefficient.json'
    surface_file = '../data_3D/geometry/element_surface.vtu'
    crack_edge = '../data_3D/geometry/crack_edge.vtu'
    output_path = '../data_3D/result/'


class Variable:
    cover_number = 0
    element_number = 0
    surface_number = 0
    crack_surface_number = 0
    crack_edge_number = 0


class DataStructure(object):
    def __init__(self):
        self.__vtk_manifold_element = NmmObjectBase('manifold_element')
        self.__vtk_physical_cover = NmmObjectBase('physical_cover')
        self.__vtk_crack_surface = NmmObjectBase('crack_surface')
        self.__relationship_element_cover = NmmObjectBase('relationship_element_cover')
        self.__special_point = NmmObjectBase('special_point')
        self.__element_surface = NmmObjectBase('element_surface')
        self.__crack_edge = NmmObjectBase('crack_edge')

    @property
    def manifold_element(self):
        return self.__vtk_manifold_element

    @manifold_element.setter
    def manifold_element(self, manifold_element):
        self.__vtk_manifold_element.content = manifold_element

    @property
    def physical_cover(self):
        return self.__vtk_physical_cover

    @physical_cover.setter
    def physical_cover(self, physical_cover):
        self.__vtk_physical_cover.content = physical_cover

    @property
    def crack_surface(self):
        return self.__vtk_crack_surface

    @crack_surface.setter
    def crack_surface(self, crack_surface):
        self.__vtk_crack_surface.content = crack_surface

    @property
    def relationship_element_cover(self):
        return self.__relationship_element_cover

    @relationship_element_cover.setter
    def relationship_element_cover(self, database):
        self.__relationship_element_cover.content = database

    @property
    def special_point(self):
        return self.__special_point

    @special_point.setter
    def special_point(self, special_point):
        self.__special_point.content = special_point

    @property
    def element_surface(self):
        return self.__element_surface

    @element_surface.setter
    def element_surface(self, element_surface):
        self.__element_surface.content = element_surface

    @property
    def crack_edge(self):
        return self.__crack_edge

    @crack_edge.setter
    def crack_edge(self, value):
        self.__crack_edge.content = value


class CrackList(object):
    element_list = None
    surface_list = None
    crack_surface_list = None
    crack_edge_list = None
