import numpy as np
import math
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader, vtkXMLPolyDataWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkQuad, vtkTriangle, vtkCell, vtkPlane, vtkPolyData
from vtkmodules.vtkCommonCore import vtkPoints
from NMM.base.ModifyVtkCell import insert_a_cell_0
from NMM.base.CopyFunction import copy_vtk_cell
from NMM.base.CalculateArea import calculate_area

def check_dihedral_angle_0(u_grid_0: vtkUnstructuredGrid):
    cell_0: vtkCell= u_grid_0.GetCell(0)
    cell_0 = copy_vtk_cell(cell_0, u_grid_0.GetPoints())

    cell_1: vtkCell= u_grid_0.GetCell(1)
    cell_1 = copy_vtk_cell(cell_1, u_grid_0.GetPoints())

    new_grid = vtkUnstructuredGrid()
    insert_a_cell_0(new_grid, cell_0)
    insert_a_cell_0(new_grid, cell_1)

    cell_0: vtkCell = new_grid.GetCell(0)
    cell_1: vtkCell = new_grid.GetCell(1)

    id_list_0 = [cell_0.GetPointId(i) for i in range(cell_0.GetNumberOfPoints())]
    id_list_1 = [cell_1.GetPointId(i) for i in range(cell_1.GetNumberOfPoints())]

    same_point_list = list(set(id_list_0).intersection(set(id_list_1)))
    different_list_0 = list(set(id_list_0).difference(set(id_list_1)))
    different_list_1 = list(set(id_list_1).difference(set(id_list_0)))

    points: vtkPoints = new_grid.GetPoints()
    normal_0 = [0, 0, 0]
    vtkTriangle.ComputeNormal(points.GetPoint(same_point_list[0]), points.GetPoint(same_point_list[1]), points.GetPoint(different_list_0[0]), normal_0)
    normal_1 = [0, 0, 0]
    vtkTriangle.ComputeNormal(points.GetPoint(same_point_list[0]), points.GetPoint(same_point_list[1]), points.GetPoint(different_list_1[0]), normal_1)

    # print(np.dot(normal_0, normal_1))
    if np.dot(normal_0, normal_1) > 0:
        return False
    else:
        return True


if __name__ == '__main__':
    reader_0 = vtkXMLUnstructuredGridReader()
    reader_0.SetFileName('error_0.vtu')
    reader_0.Update()
    u_grid_0: vtkUnstructuredGrid = reader_0.GetOutput()
    cell_0: vtkQuad = u_grid_0.GetCell(0)
    cell_0 = copy_vtk_cell(cell_0, u_grid_0.GetPoints())
    area_0 = calculate_area(cell_0.GetPoints())

    cell_1: vtkTriangle = u_grid_0.GetCell(1)
    cell_1 = copy_vtk_cell(cell_1, u_grid_0.GetPoints())
    area_1 = calculate_area(cell_1.GetPoints())
    if not area_1 > 0.00001:
        print(area_1)

    # check_dihedral_angle_0(u_grid_0)


