from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPolygon, VTK_POLYHEDRON, vtkGenericCell
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints


def get_polyhedron_list(vtk_cell: vtkCell, vtk_points: vtkPoints):
    # temp_cell_point is a dictionary consist of face new id and face_point_list
    temp_old_id_point = {}
    for each_face in range(vtk_cell.GetNumberOfFaces()):
        temp_face: vtkPolygon = vtk_cell.GetFace(each_face)
        face_id_list: vtkIdList = temp_face.GetPointIds()
        for each_point in range(temp_face.GetNumberOfPoints()):
            temp_id = face_id_list.GetId(each_point)
            temp_coord = vtk_points.GetPoint(temp_id)
            temp_old_id_point[temp_id] = temp_coord

    temp_new_id_point = {}
    temp_old_new_id = {}
    for each_new_id, each_old_id in enumerate(temp_old_id_point.keys()):
        temp_new_id_point[each_new_id] = temp_old_id_point[each_old_id]
        temp_old_new_id[each_old_id] = each_new_id

    id_list = vtkIdList()
    id_list.InsertNextId(vtk_cell.GetNumberOfFaces())
    for each_face in range(vtk_cell.GetNumberOfFaces()):
        temp_face: vtkPolygon = vtk_cell.GetFace(each_face)
        id_list.InsertNextId(temp_face.GetNumberOfPoints())
        face_id_list: vtkIdList = temp_face.GetPointIds()
        for each_point in range(temp_face.GetNumberOfPoints()):
            temp_old_id = face_id_list.GetId(each_point)
            id_list.InsertNextId(temp_old_new_id[temp_old_id])

    id_point_dict = temp_new_id_point
    return id_list, id_point_dict


def copy_polyhedron(vtk_cell: vtkCell, vtk_points: vtkPoints):
    id_list, id_point_dict = get_polyhedron_list(vtk_cell, vtk_points)

    u_grid = vtkUnstructuredGrid()
    temp_point_list = vtkPoints()
    u_grid.SetPoints(temp_point_list)

    temp_points = vtkPoints()
    temp_points.DeepCopy(vtk_cell.GetPoints())

    grid_points = vtkPoints()
    grid_points.ShallowCopy(u_grid.GetPoints())

    for each_point in range(vtk_cell.GetNumberOfPoints()):
        temp_point = id_point_dict[each_point]
        grid_points.InsertNextPoint(temp_point)
    u_grid.InsertNextCell(VTK_POLYHEDRON, id_list)

    temp_cell = u_grid.GetCell(0)
    # temp_u_list = u_grid.GetPoints()
    # print('__________in__________')
    # print(temp_cell.GetPoints().GetPoint(0))
    # print(vtk_cell.GetPoints().GetPoint(0))
    # print(temp_u_list.GetPoint(0))

    return temp_cell


def copy_vtk_cell(vtk_cell: vtkCell, vtk_points: vtkPoints):
    new_id_list = vtkIdList()
    new_points = vtkPoints()
    id_list: vtkIdList = vtk_cell.GetPointIds()
    for each_Id in range(vtk_cell.GetNumberOfPoints()):
        new_id_list.InsertNextId(each_Id)
        old_id = id_list.GetId(each_Id)
        point = vtk_points.GetPoint(old_id)
        new_points.InsertNextPoint(point)

    new_cell = vtkGenericCell()
    new_cell.SetCellType(vtk_cell.GetCellType())
    new_cell.SetPoints(new_points)
    new_cell.SetPointIds(new_id_list)

    return new_cell


