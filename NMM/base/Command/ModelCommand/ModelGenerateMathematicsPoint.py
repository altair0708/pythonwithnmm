from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.GenerateGrid.GenerateMathematicsPoint import GenerateMathematicsPoint
from NMM.base.VTKBase.get_a_vtk_cell_grid_1 import get_a_vtk_cell_grid
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell


class ModelGenerateMathematicsPoint(AbstractCommand):
    def __init__(self, data_structure: DataStructure):
        self.__data_structure = data_structure

    def execute(self):
        geometry_tetrahedron: VtkGrid = self.__data_structure.get_property('geometric_tetrahedron')
        mathematics_point: VtkGrid = self.__data_structure.get_property('mathematics_point')
        generator = GenerateMathematicsPoint(geometry_tetrahedron, mathematics_point)
        generator.update()
