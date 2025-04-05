from NMM.base.VTKBase import new_a_grid, get_attribute
from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import relationship_cache
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellArray, vtkPointData, vtkVertex
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkIntArray


class GenerateMathematicsPoint(AbstractAlgorithm):
    def __init__(self, geometric_tetrahedron: VtkGrid, mathematics_point: VtkGrid):
        self.__geometric_tetrahedron = geometric_tetrahedron
        self.__mathematics_point = mathematics_point

    def update(self, *args, **kwargs) -> None:
        vtk_model = self.__geometric_tetrahedron.value
        point_data: vtkPointData = vtk_model.GetPointData()
        cover_id = vtkIntArray()
        cover_id.DeepCopy(point_data.GetArray('point_id'))
        cover_id.SetName('cell_id')

        points = vtkPoints()
        points.DeepCopy(vtk_model.GetPoints())

        cover_grid = new_a_grid()
        cover_grid.SetPoints(points)
        for each_cover_id in range(points.GetNumberOfPoints()):
            vtk_vertex = vtkVertex()
            vtk_vertex.GetPointIds().SetId(0, each_cover_id)
            cover_grid.InsertNextCell(vtk_vertex.GetCellType(), vtk_vertex.GetPointIds())
        cover_grid.GetCellData().AddArray(cover_id)

        # add relationship cache of cover-element
        for each_cover_id in range(cover_grid.GetNumberOfCells()):
            assert get_attribute(cover_grid, 'cell_id', each_cover_id)[0] == each_cover_id
            assert get_attribute(vtk_model, 'point_id', each_cover_id)[0] == each_cover_id
            cell_id_list = vtkIdList()
            vtk_model.GetPointCells(each_cover_id, cell_id_list)
            for each_id in range(cell_id_list.GetNumberOfIds()):
                each_cell_id = cell_id_list.GetId(each_id)
                assert get_attribute(vtk_model, 'cell_id', each_cell_id)[0] == each_cell_id
                relationship_cache.add_item('cover', each_cover_id, 'element', each_cell_id)

        self.__mathematics_point.value = cover_grid
