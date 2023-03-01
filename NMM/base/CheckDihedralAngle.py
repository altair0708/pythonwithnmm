import sys
from NMM.base.WriteErrorVTU import write_error_vtu
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPlane, vtkPolyData, vtkPolygon, vtkGenericCell, vtkLine, vtkDataSet
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkMath
from vtkmodules.vtkFiltersCore import vtkCutter


def generate_vector(vtk_grid, id_0, id_1):
    result = (vtk_grid.GetPoint(id_0)[0] - vtk_grid.GetPoint(id_1)[0],
              vtk_grid.GetPoint(id_0)[1] - vtk_grid.GetPoint(id_1)[1],
              vtk_grid.GetPoint(id_0)[2] - vtk_grid.GetPoint(id_1)[2])
    return result


def check_dihedral_angle(u_grid: vtkDataSet):

    assert u_grid.GetNumberOfCells() == 2
    if u_grid.GetDataObjectType() == 4:
        new_grid = vtkUnstructuredGrid()
        new_grid.DeepCopy(u_grid)
    elif u_grid.GetDataObjectType() == 0:
        new_grid = vtkPolyData()
        new_grid.DeepCopy(u_grid)
    else:
        raise Exception('DataSet type error')

    cell_0 = vtkGenericCell()
    cell_0.DeepCopy(u_grid.GetCell(0))
    cell_1 = vtkGenericCell()
    cell_1.DeepCopy(u_grid.GetCell(1))

    id_list_0 = vtkIdList()
    id_list_0.DeepCopy(cell_0.GetPointIds())

    id_list_1 = vtkIdList()
    id_list_1.DeepCopy(cell_1.GetPointIds())

    id_list_0.IntersectWith(id_list_1)
    try:
        assert id_list_0.GetNumberOfIds() == 2
    except AssertionError:
        write_error_vtu(new_grid, 1)
        print(new_grid.GetNumberOfPoints())
        sys.exit()

    point_0 = u_grid.GetPoints().GetPoint(id_list_0.GetId(0))
    point_1 = u_grid.GetPoints().GetPoint(id_list_0.GetId(1))

    point_2 = ((point_0[0] + point_1[0]) / 2, (point_0[1] + point_1[1]) / 2, (point_0[2] + point_1[2]) / 2)
    vector_0 = (point_0[0] - point_1[0], point_0[1] - point_1[1], point_0[2] - point_1[2])

    # print(point_2)
    # print(vector_0)

    plane = vtkPlane()
    plane.SetNormal(vector_0)
    plane.SetOrigin(point_2)

    cutter = vtkCutter()
    cutter.SetInputData(new_grid)
    cutter.SetCutFunction(plane)
    cutter.Update()
    angle: vtkPolyData = cutter.GetOutput()

    double_id_list = []
    for each_cell_id in range(angle.GetNumberOfCells()):
        temp_id_list = vtkIdList()
        temp_id_list.DeepCopy(angle.GetCell(each_cell_id).GetPointIds())
        for each_point_id in range(temp_id_list.GetNumberOfIds()):
            double_id_list.append(temp_id_list.GetId(each_point_id))

    single_id_list = [i for i in range(angle.GetNumberOfPoints())]

    for each_point_id in single_id_list:
        double_id_list.remove(each_point_id)

    for each_point_id in double_id_list:
        cell_id_list = vtkIdList()
        angle.GetPointCells(each_point_id, cell_id_list)

        vector_list = []
        for each_cell_sequence in range(cell_id_list.GetNumberOfIds()):
            temp_cell_id = cell_id_list.GetId(each_cell_sequence)
            temp_cell = vtkGenericCell()
            temp_cell.DeepCopy(angle.GetCell(temp_cell_id))

            assert temp_cell.GetNumberOfPoints() == 2
            end_point_id = temp_cell.GetPointId(0)
            if end_point_id == each_point_id:
                end_point_id = temp_cell.GetPointId(1)
            vector_list.append(generate_vector(angle, end_point_id, each_point_id))

        assert len(vector_list) == 2
        if vtkMath.Dot(vector_list[0], vector_list[1]) >= 0:
            return False
    return True


if __name__ == '__main__':

    polygon_0 = vtkPolygon()
    polygon_0.GetPointIds().SetNumberOfIds(4)
    polygon_0.GetPointIds().SetId(0, 0)
    polygon_0.GetPointIds().SetId(1, 1)
    polygon_0.GetPointIds().SetId(2, 2)
    polygon_0.GetPointIds().SetId(3, 3)

    polygon_1 = vtkPolygon()
    polygon_1.GetPointIds().SetNumberOfIds(4)
    polygon_1.GetPointIds().SetId(0, 2)
    polygon_1.GetPointIds().SetId(1, 3)
    polygon_1.GetPointIds().SetId(2, 4)
    polygon_1.GetPointIds().SetId(3, 5)

    test_points = vtkPoints()
    test_points.InsertNextPoint(-1, 1, 0)
    test_points.InsertNextPoint(-1, 0, 0)
    test_points.InsertNextPoint(0, 0, 0)
    test_points.InsertNextPoint(0, 1, 0)
    test_points.InsertNextPoint(-1, 1, 1)
    test_points.InsertNextPoint(-1, 0, 1)

    test_grid = vtkUnstructuredGrid()
    test_grid.SetPoints(test_points)
    test_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())
    test_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())

    print(check_dihedral_angle(test_grid))



