from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           vtkCell,
                                           VTK_POLYHEDRON,
                                           VTK_POLYGON,
                                           vtkPolygon,
                                           vtkTetra,
                                           VTK_TETRA,
                                           vtkEmptyCell)
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList


def insert_a_cell(vtk_model: vtkUnstructuredGrid, vtk_cell: vtkCell):
    if vtk_cell.GetCellType() == VTK_POLYHEDRON:
        if vtk_model.GetNumberOfPoints() == 0:
            new_point_list = vtkPoints()
            vtk_model.SetPoints(new_point_list)
        points_number = vtk_model.GetNumberOfPoints()

        # vtkIdList
        id_list = vtkIdList()
        id_list.InsertNextId(vtk_cell.GetNumberOfFaces())
        for each_face in range(vtk_cell.GetNumberOfFaces()):
            temp_face: vtkPolygon = vtk_cell.GetFace(each_face)
            id_list.InsertNextId(temp_face.GetNumberOfPoints())
            face_id_list: vtkIdList = temp_face.GetPointIds()
            for each_point in range(temp_face.GetNumberOfPoints()):
                temp_id = face_id_list.GetId(each_point)
                id_list.InsertNextId(temp_id + points_number)

        # vtkPoints
        cell_point_list = vtkPoints()
        cell_point_list.DeepCopy(vtk_cell.GetPoints())
        cell_point_number = cell_point_list.GetNumberOfPoints()

        model_point_list = vtkPoints()
        model_point_list.ShallowCopy(vtk_model.GetPoints())

        for each_point in range(cell_point_number):
            temp_point = cell_point_list.GetPoint(each_point)
            model_point_list.InsertNextPoint(temp_point)

        vtk_model.InsertNextCell(VTK_POLYHEDRON, id_list)

    else:
        if vtk_cell.GetCellType() == VTK_POLYGON:
            new_cell = vtkPolygon()
        elif vtk_cell.GetCellType() == VTK_TETRA:
            new_cell = vtkTetra()
        else:
            print(vtk_cell.GetCellType())
            raise Exception('type error!!!')

        if vtk_model.GetNumberOfPoints() == 0:
            new_point_list = vtkPoints()
            vtk_model.SetPoints(new_point_list)

        new_cell.DeepCopy(vtk_cell)

        model_point_list = vtkPoints()
        model_point_list.ShallowCopy(vtk_model.GetPoints())
        model_point_number = vtk_model.GetNumberOfPoints()

        cell_point_list = vtkPoints()
        cell_point_list.DeepCopy(vtk_cell.GetPoints())
        cell_point_number = cell_point_list.GetNumberOfPoints()

        for each_point in range(cell_point_number):
            temp_point = cell_point_list.GetPoint(each_point)
            model_point_list.InsertNextPoint(temp_point)
            new_cell.GetPointIds().SetId(each_point, model_point_number + each_point)
        vtk_model.InsertNextCell(new_cell.GetCellType(), new_cell.GetPointIds())

        # points_0 = vtk_cell.GetPoints()
        # points_1 = new_cell.GetPoints()
        # points_2 = vtk_model.GetPoints()
        # for i in range(4):
        #     print('__________in___________')
        #     print(points_0.GetPoint(i))
        #     print(points_1.GetPoint(i))
        #     print(points_2.GetPoint(i))


