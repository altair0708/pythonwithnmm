from NMM.base.Part.Part import Part


class DataStructure(Part):
    def __init__(self):
        super(DataStructure, self).__init__()
        self._name = 'data_structure'

    def generate_geometric_grid(self, geometric_name: str):
        self.get_property(geometric_name).value = self.get_property('gmsh_file').extract_by_cell_type(geometric_name)

    def generate_cover(self, cover_name: str):
        self.get_property(cover_name).value = self.get_property('geometric_tetrahedron').extract_mathematics_cover(cover_name)

    def add_attribute(self, grid_name: str, attribute_name: str):
        self.get_property(grid_name).add_attribute(attribute_name)

    def write_file(self, grid_name: str, file_path: str):
        self.get_property(grid_name).write_file(file_path)

