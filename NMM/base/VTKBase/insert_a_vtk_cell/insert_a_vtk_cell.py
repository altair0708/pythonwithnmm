from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron, VTK_POLYHEDRON
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_point import insert_a_point


def insert_a_vtk_cell(cell_grid: vtkUnstructuredGrid, target_grid: vtkUnstructuredGrid):

    assert cell_grid.GetNumberOfCells() == 1

    cell_id = vtkIdList()
    cell_points: vtkPoints = cell_grid.GetPoints()
    cell_grid.GetCellPoints(0, cell_id)

    # insert points
    cell_id_dict = {}
    new_cell_id = vtkIdList()
    for each in range(cell_id.GetNumberOfIds()):
        point_id = cell_id.GetId(each)
        new_point_id = insert_a_point(target_grid, cell_points.GetPoint(point_id))
        new_cell_id.InsertNextId(new_point_id)
        # transform from cell_grid to target_grid
        cell_id_dict[point_id] = new_point_id

    # polyhedron
    if cell_grid.GetCellType(0) == VTK_POLYHEDRON:
        face_id = vtkIdList()
        temp_list = []
        cell_grid.GetFaceStream(0, face_id)
        for x in range(face_id.GetNumberOfIds()):
            temp_list.append(face_id.GetId(x))

        new_face_id = vtkIdList()
        # face_number
        new_face_id.InsertNextId(temp_list[0])
        for each_face in range(temp_list.pop(0)):
            # point_number of one face
            new_face_id.InsertNextId(temp_list[0])
            for each_point in range(temp_list.pop(0)):
                # point_id
                new_face_id.InsertNextId(cell_id_dict[temp_list.pop(0)])

        new_cell_id = vtkIdList()
        new_cell_id.DeepCopy(new_face_id)

    # insert cell
    target_grid.InsertNextCell(cell_grid.GetCellType(0), new_cell_id)
