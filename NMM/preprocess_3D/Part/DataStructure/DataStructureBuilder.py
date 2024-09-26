from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure
from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Command.ModelCommand.ModelGetPath import ModelGetPath
from NMM.base.Command.Invoker import Invoker


class DataStructureBuilder(AbstractConstructor):
    def build(self):
        data_structure = DataStructure()  # singleton

        mesh_grid = ['gmsh_file', 'special_point', 'initial_crack']
        for each_grid in mesh_grid:
            temp_grid = VtkGrid(each_grid, self.get_path(each_grid))
            data_structure.add_property(temp_grid)

        add_grid = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron',
                    'mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface',
                    'crack_surface', 'crack_edge', 'new_element', 'new_cover', 'new_surface']
        for each_grid in add_grid:
            temp_grid = VtkGrid(each_grid)
            data_structure.add_property(temp_grid)

        return data_structure

    @staticmethod
    def get_path(path_name: str):
        from NMM.preprocess_3D.Model.Model import preprocess_model
        path_part = preprocess_model.get_property('file_path')

        invoker = Invoker(ModelGetPath(path_name, path_part))
        return invoker.press_button()

