from NMM.base.VTKBase.VTKBaseInterface import AbstractVTKBase
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPointLocator
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader
import sys


class VTKBase(AbstractVTKBase):
    @staticmethod
    def insert_a_grid(vtk_model: vtkUnstructuredGrid, new_vtk_model: vtkUnstructuredGrid):
        pass

    @staticmethod
    def insert_a_grid_0(vtk_model: vtkUnstructuredGrid, new_vtk_model: vtkUnstructuredGrid):
        pass

    @staticmethod
    def get_a_vtk_cell_grid(vtk_model: vtkUnstructuredGrid, id_value: int):
        # cell type
        cell_type = vtk_model.GetCellType(id_value)

        # id list
        cell_id_list = vtkIdList()
        if 42 == cell_type:
            # polyhedron
            vtk_model.GetFaceStream(id_value, cell_id_list)
        else:
            # other vtk_cell
            cell_id_list.DeepCopy(vtk_model.GetCell(id_value).GetPointIds())

        # cell points
        cell_points = vtkPoints()
        cell_points.DeepCopy(vtk_model.GetPoints())

        new_grid = vtkUnstructuredGrid()
        new_grid.InsertNextCell(cell_type, cell_id_list)
        new_grid.SetPoints(cell_points)

        return new_grid

    @staticmethod
    def insert_unique_point_grid(vtk_model: vtkUnstructuredGrid, point=(0, 0, 0)):

        merger = vtkPointLocator()
        merger.SetDataSet(vtk_model)
        merger.InitPointInsertion(vtk_model.GetPoints(), vtk_model.GetBounds())
        merger.BuildLocator()

        point_id_list = vtkIdList()
        merger.FindPointsWithinRadius(0.001, point, point_id_list)
        try:
            # TODO
            # assert point_id_list.GetNumberOfIds() < 2
            assert point_id_list.GetNumberOfIds() < 10
        except AssertionError:
            sys.exit()

        if point_id_list.GetNumberOfIds() == 0:
            point_id = vtk_model.GetNumberOfPoints()
            vtk_model.GetPoints().InsertNextPoint(point)
        else:
            point_id = point_id_list.GetId(0)

        return point_id

    @staticmethod
    def load_a_grid(file_name):
        reader = vtkXMLUnstructuredGridReader()
        reader.SetFileName(file_name)
        reader.Update()
        return reader.GetOutput()

    @staticmethod
    def write_a_grid(vtk_grid, file_name):
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetInputData(vtk_grid)
        writer.SetFileName(file_name)
        writer.Write()

    @staticmethod
    def new_a_grid():
        new_grid = vtkUnstructuredGrid()
        points = vtkPoints()
        new_grid.SetPoints(points)
        return new_grid


