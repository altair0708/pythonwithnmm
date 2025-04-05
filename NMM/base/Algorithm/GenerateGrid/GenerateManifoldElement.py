from NMM.base.VTKBase import new_a_grid, get_attribute
from NMM.base.VTKBase.get_a_vtk_cell_grid_1 import get_a_vtk_cell_grid
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell
from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import relationship_cache
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellArray, vtkPointData, vtkVertex
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkIntArray


class GenerateManifoldElement(AbstractAlgorithm):
    def __init__(self, geometric_tetrahedron: VtkGrid, manifold_element: VtkGrid):
        self.__geometric_tetrahedron = geometric_tetrahedron
        self.__manifold_element = manifold_element

    def update(self, *args, **kwargs):
        vtk_model = self.__geometric_tetrahedron.value
        new_grid = new_a_grid()
        for each_cell in range(vtk_model.GetNumberOfCells()):
            vtk_cell = get_a_vtk_cell_grid(vtk_model, each_cell, turn_polyhedron=True)
            new_grid = insert_a_vtk_cell(new_grid, vtk_cell)

        self.__manifold_element.value = new_grid
        for each_element_id in range(self.__manifold_element.get_cell_number()):
            assert self.__manifold_element.get_attribute('cell_id', each_element_id)[0] == self.__geometric_tetrahedron.get_attribute('cell_id', each_element_id)[0]

            manifold_point_id = self.__manifold_element.get_cell_point_id(each_element_id)
            tetrahedron_point_id = self.__geometric_tetrahedron.get_cell_point_id(each_element_id)

            set_0 = set()
            set_1 = set()
            for each_point_id_0, each_point_id_1 in zip(manifold_point_id, tetrahedron_point_id):
                set_0.add(self.__manifold_element.get_point_attribute('point_id', each_point_id_0)[0])
                set_1.add(self.__geometric_tetrahedron.get_point_attribute('point_id', each_point_id_1)[0])
            assert set_0 == set_1
