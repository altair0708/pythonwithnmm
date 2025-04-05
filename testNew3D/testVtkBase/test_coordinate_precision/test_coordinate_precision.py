from NMM.base.VTKBase import new_a_grid, load_a_grid, write_file, get_point_coordinate, get_cell_point_id
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell
from NMM.base.VTKBase.get_a_vtk_cell_grid_1 import get_a_vtk_cell_grid
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellArray, vtkPointData, vtkVertex
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkIntArray
import numpy as np


def test_coordinate_precision():
    print('')
    vtk_model = load_a_grid('geometric_tetrahedron.vtu')

    point_data: vtkPointData = vtk_model.GetPointData()

    cover_id = vtkIntArray()
    cover_id.DeepCopy(point_data.GetArray('point_id'))
    cover_id.SetName('cover_id')

    points = vtkPoints()
    points.DeepCopy(vtk_model.GetPoints())

    cover_grid = new_a_grid()
    cover_grid.SetPoints(points)
    cover_grid.GetPointData().AddArray(cover_id)
    for each_cover_id in range(points.GetNumberOfPoints()):
        vtk_vertex = vtkVertex()
        vtk_vertex.GetPointIds().SetId(0, each_cover_id)
        cover_grid.InsertNextCell(vtk_vertex.GetCellType(), vtk_vertex.GetPointIds())
    cover_grid.GetCellData().AddArray(cover_id)
    write_file(cover_grid, 'cover_grid.vtu')

    new_grid = new_a_grid()
    for each_cell in range(vtk_model.GetNumberOfCells()):
        vtk_cell = get_a_vtk_cell_grid(vtk_model, each_cell, turn_polyhedron=True)
        new_grid = insert_a_vtk_cell(vtk_cell, new_grid)
    cell_0: vtkUnstructuredGrid = get_a_vtk_cell_grid(vtk_model, 0, turn_polyhedron=True)
    write_file(cell_0, 'cell_0.vtu')
    write_file(new_grid, 'new_grid.vtu')

    # vtk_cell_0 = cell_0.GetCell(0)
    # print([cell_0.GetPoint(vtk_cell_0.GetPointId(i)) for i in range(vtk_cell_0.GetNumberOfPoints())])
    # print([vtk_cell_0.GetPointId(i) for i in range(vtk_cell_0.GetNumberOfPoints())])
    #
    # id_list = vtkIdList()
    # cell_0.GetFaceStream(0, id_list)
    # print([id_list.GetId(i) for i in range(id_list.GetNumberOfIds())])
    #
    # vtk_cell_1 = vtk_model.GetCell(0)
    # print([vtk_model.GetPoint(vtk_cell_1.GetPointId(i)) for i in range(vtk_cell_1.GetNumberOfPoints())])
    # print([vtk_cell_1.GetPointId(i) for i in range(vtk_cell_1.GetNumberOfPoints())])
    #
    # old_point_id = get_cell_point_id(vtk_model, 0)
    # cell_point_id = get_cell_point_id(cell_0, 0)
    # new_point_id = get_cell_point_id(new_grid, 0)
    #
    # for each_old_id, each_new_id, each_cell_id in zip(old_point_id, new_point_id, cell_point_id):
    #     old_coordinate = get_point_coordinate(vtk_model, each_old_id)
    #     cell_coordinate = get_point_coordinate(cell_0, each_cell_id)
    #     new_coordinate = get_point_coordinate(new_grid, each_new_id)
    #     print('**************')
    #     print(old_coordinate)
    #     print(cell_coordinate)
    #     print(new_coordinate)
    #     print(np.array(cell_coordinate, dtype=np.float64) - np.array(new_coordinate, dtype=np.float64))
    #
    # write_file(cell_0, 'cell_0.vtu')
    # write_file(new_grid, 'new_grid.vtu')
    #
    #
