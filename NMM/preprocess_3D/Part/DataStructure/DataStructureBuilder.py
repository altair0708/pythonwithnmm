from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure
from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Command.ModelCommand.ModelGetPath import ModelGetPath
from NMM.base.Command.Invoker import Invoker


class DataStructureBuilder(AbstractConstructor):
    def build(self):
        data_structure = DataStructure()  # singleton

        gmsh_grid = VtkGrid('gmsh_file', self.get_path('gmsh_file'))
        data_structure.add_property(gmsh_grid)

        special_point_grid = VtkGrid('special_point', self.get_path('special_point'))
        data_structure.add_property(special_point_grid)

        initial_crack_grid = VtkGrid('initial_crack', self.get_path('initial_crack'))
        data_structure.add_property(initial_crack_grid)

        add_grid = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron',
                    'mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface',
                    'crack_surface', 'crack_edge', 'new_element']
        for each_grid in add_grid:
            temp_grid = VtkGrid(each_grid)
            data_structure.add_property(temp_grid)

        return data_structure

    @staticmethod
    def get_path(path_name: str):
        from NMM.preprocess_3D.Model.Model import PreprocessModel
        path_part = PreprocessModel().get_property('file_path')

        invoker = Invoker(ModelGetPath(path_name, path_part))
        return invoker.press_button()

