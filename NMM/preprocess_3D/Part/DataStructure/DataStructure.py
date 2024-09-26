from NMM.base.Part.Part import Part
from NMM.base.Algorithm.InitialCrackGenerator import InitialCrackGenerator
import warnings


class DataStructure(Part):

    """
    Relationship of entity:

    new_cover --- new_element --- new_surface
        |               |               |
    cover     ---    element  ---    surface
                       |               |
                crack_surface --- crack_edge
    """

    def __init__(self):
        super(DataStructure, self).__init__()
        self.name = 'data_structure'

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
        else:
            raise Exception(f'Entity name error: {entity_name}!!!')

    def initial_crack_generate(self):
        initial_crack = self.get_property('initial_crack')
        new_cover_grid = self.get_property('new_cover')
        new_element_grid = self.get_property('new_element')
        new_surface_grid = self.get_property('new_surface')
        mathematics_point_grid = self.get_property('mathematics_point')
        manifold_element_grid = self.get_property('manifold_element')
        element_surface_grid = self.get_property('element_surface')
        crack_surface_grid = self.get_property('crack_surface')
        crack_edge_grid = self.get_property('crack_edge')

        crack_mediator = InitialCrackGenerator(initial_crack,
                                               new_cover_grid, new_element_grid, new_surface_grid,
                                               mathematics_point_grid, manifold_element_grid, element_surface_grid,
                                               crack_surface_grid, crack_edge_grid)
        crack_mediator.update()

    def add_attribute(self, grid_name: str, attribute_name: str):
        self.get_property(grid_name).add_attribute(attribute_name)

    def write_file(self, grid_name: str):
        self.get_property(grid_name).write_file()


