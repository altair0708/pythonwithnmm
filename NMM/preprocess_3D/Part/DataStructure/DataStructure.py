from NMM.base.Part.Part import Part
from NMM.base.Algorithm.CrackGenerator import CrackGenerator
import warnings


class DataStructure(Part):
    def __init__(self):
        super(DataStructure, self).__init__()
        self._name = 'data_structure'

    def generate_geometric_grid(self, geometric_name: str):
        warnings.warn('Deprecation method: generate_geometric_grid', DeprecationWarning)
        self.get_property(geometric_name).value = self.get_property('gmsh_file').extract_by_cell_type(geometric_name)

    def generate_cover(self, cover_name: str):
        warnings.warn('Deprecation method: generate_cover', DeprecationWarning)
        self.get_property(cover_name).value = self.get_property('geometric_tetrahedron').extract_mathematics_cover(cover_name)

    def generate_grid(self, entity_name: str):
        entity_list = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron']
        cover_list = ['mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface']
        crack_list = ['crack_surface', 'crack_edge']
        if entity_name in entity_list:
            name = 'gmsh_file'
            self.get_property(entity_name).value = self.get_property(name).generate_grid(entity_name)
        elif entity_name in cover_list:
            name = 'geometric_tetrahedron'
            self.get_property(entity_name).value = self.get_property(name).generate_grid(entity_name)
        elif entity_name in crack_list:
            initial_crack = self.get_property('initial_crack')
            crack_grid = self.get_property(entity_name)
            if 'crack_surface' == entity_name:
                element_grid = self.get_property('manifold_element')
            elif 'crack_edge' == entity_name:
                element_grid = self.get_property('element_surface')
            else:
                raise Exception('Entity name error!!!')
            crack_mediator = CrackGenerator(initial_crack, element_grid, crack_grid)
            crack_mediator.update(entity_name)
        else:
            raise Exception('Entity name error!!!')

    def add_attribute(self, grid_name: str, attribute_name: str):
        self.get_property(grid_name).add_attribute(attribute_name)

    def write_file(self, grid_name: str, file_path: str):
        self.get_property(grid_name).write_file(file_path)


