import sys

from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           vtkMergePoints,
                                           vtkPointLocator,
                                           vtkDataSet,
                                           vtkCell,
                                           VTK_POLYHEDRON,
                                           VTK_POLYGON,
                                           vtkPolygon,
                                           vtkTetra,
                                           vtkGenericCell,
                                           VTK_TETRA,
                                           vtkEmptyCell)
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, mutable, vtkMath
from NMM.GlobalVariable import CONST


# this method will lead to duplicated point
def insert_a_cell(vtk_model: vtkUnstructuredGrid, vtk_cell: vtkCell):

    # insert a deep copy cell of given vtkCell

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
            new_cell = vtkGenericCell()
            new_cell.SetCellType(vtk_cell.GetCellType())

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

        # don't merge the coincide points
        for each_point in range(cell_point_number):
            temp_point = cell_point_list.GetPoint(each_point)
            model_point_list.InsertNextPoint(temp_point)
            new_cell.GetPointIds().SetId(each_point, model_point_number + each_point)
        vtk_model.InsertNextCell(new_cell.GetCellType(), new_cell.GetPointIds())

        # try to merge the coincide points

        # points_0 = vtk_cell.GetPoints()
        # points_1 = new_cell.GetPoints()
        # points_2 = vtk_model.GetPoints()
        # for i in range(4):
        #     print('__________in___________')
        #     print(points_0.GetPoint(i))
        #     print(points_1.GetPoint(i))
        #     print(points_2.GetPoint(i))


# this method will not lead to duplicated point
def insert_a_cell_0(vtk_model: vtkUnstructuredGrid, vtk_cell: vtkCell):
    if vtk_cell.GetCellType() == VTK_POLYGON:
        new_cell = vtkPolygon()
    elif vtk_cell.GetCellType() == VTK_TETRA:
        new_cell = vtkTetra()
    else:
        new_cell = vtkGenericCell()
        new_cell.SetCellType(vtk_cell.GetCellType())

    if vtk_model.GetNumberOfPoints() == 0:
        new_point_list = vtkPoints()
        new_point_list.InsertNextPoint(0, 0, 0)
        vtk_model.SetPoints(new_point_list)

    new_cell.DeepCopy(vtk_cell)

    model_point_list = vtkPoints()
    model_point_list.ShallowCopy(vtk_model.GetPoints())
    model_point_number = vtk_model.GetNumberOfPoints()

    # merger = vtkMergePoints()
    merger = vtkPointLocator()
    merger.SetTolerance(CONST.TOLERANCE)
    merger.SetDataSet(vtk_model)
    merger.InitPointInsertion(vtk_model.GetPoints(), vtk_model.GetBounds())
    merger.BuildLocator()

    cell_point_list = vtkPoints()
    cell_point_list.DeepCopy(vtk_cell.GetPoints())
    cell_point_number = cell_point_list.GetNumberOfPoints()

    # merge the coincide points
    new_point_number = 0
    for each_point in range(cell_point_number):

        temp_point = cell_point_list.GetPoint(each_point)

        point_id_list = vtkIdList()
        merger.FindPointsWithinRadius(0.001, temp_point, point_id_list)
        try:
            # TODO
            # assert point_id_list.GetNumberOfIds() < 2
            assert point_id_list.GetNumberOfIds() < 10
        except AssertionError:
            print(point_id_list.GetNumberOfIds())
            sys.exit()

        # if result != -1:
        #     close_point = model_point_list.GetPoint(result)
        #     if vtkMath.Distance2BetweenPoints(temp_point, close_point) > CONST.TOLERANCE:
        #         a = new_point_number + model_point_number
        #         model_point_list.InsertNextPoint(temp_point)
        #         new_point_number = new_point_number + 1
        #     else:
        #         a = result
        # # vtkPoints have no point
        # else:
        #     a = 0
        #     model_point_list.InsertNextPoint(temp_point)
        #     new_point_number = new_point_number + 1

        if point_id_list.GetNumberOfIds() == 0:
            a = new_point_number + model_point_number
            model_point_list.InsertNextPoint(temp_point)
            new_point_number = new_point_number + 1
        else:
            a = point_id_list.GetId(0)
        # print(a)
        new_cell.GetPointIds().SetId(each_point, a)
    vtk_model.InsertNextCell(new_cell.GetCellType(), new_cell.GetPointIds())
