from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader, vtkXMLPolyDataWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPlane, vtkPolyData, vtkPolygon, vtkGenericCell, vtkLine
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkMath
from vtkmodules.vtkFiltersCore import vtkCutter


def generate_vector(vtk_grid, id_0, id_1):
    result = (vtk_grid.GetPoint(id_0)[0] - vtk_grid.GetPoint(id_1)[0],
              vtk_grid.GetPoint(id_0)[1] - vtk_grid.GetPoint(id_1)[1],
              vtk_grid.GetPoint(id_0)[2] - vtk_grid.GetPoint(id_1)[2])
    return result


def check_dihedral_angle(u_grid: vtkUnstructuredGrid):

    assert u_grid.GetNumberOfCells() == 2
    new_grid = vtkUnstructuredGrid()
    new_grid.DeepCopy(u_grid)

    cell_0 = vtkGenericCell()
    cell_0.DeepCopy(u_grid.GetCell(0))
    cell_1 = vtkGenericCell()
    cell_1.DeepCopy(u_grid.GetCell(1))

    id_list_0 = vtkIdList()
    id_list_0.DeepCopy(cell_0.GetPointIds())
    id_list_1 = vtkIdList()
    id_list_1.DeepCopy(cell_1.GetPointIds())

    id_list_0.IntersectWith(id_list_1)
    assert id_list_0.GetNumberOfIds() == 2

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

    result_list = []

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



