from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPolyData, vtkPolygon
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter


def get_polyhedron_by_point(point_id: int, vtk_model: vtkUnstructuredGrid):

    """
    This function is used to generate mathematics/physics cover temporarily
    We can begin with a point in vtkUnstructuredGrid
    First we find all cells shared the selected point
    Secondly we generate a wrapped polyhedron of all cells
    At last we return the FaceIdList of the polyhedron, FaceIdList is a special cell in vtkUnstructuredGrid

    If want to use this function, please ensure the two vtkUnstructuredGrid have the same vtkPoints
    one is vtk_model of parameters, the other is the FaceIdList which you want to insert.

    para: point_id, point id in vtkUnstructuredGrid
    vtk_model, vtkUnstructuredGrid to be processed
    """

    cellIdList = vtkIdList()
    vtk_model.GetPointCells(point_id, cellIdList)

    # Generate new grid of selected cell
    mathGrid = vtkUnstructuredGrid()
    idNumber = cellIdList.GetNumberOfIds()
    for eachId in range(idNumber):
        cellId = cellIdList.GetId(eachId)
        tempCell: vtkCell = vtk_model.GetCell(cellId)
        mathGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
    mathGrid.SetPoints(vtk_model.GetPoints())

    surface = vtkGeometryFilter()
    surface.PassThroughPointIdsOn()
    surface.SetInputData(mathGrid)
    surface.MergingOff()
    surface.Update()
    result: vtkPolyData = surface.GetOutput()

    faceIdList = vtkIdList()
    faceIdList.InsertNextId(result.GetNumberOfCells())
    for face_id in range(result.GetNumberOfCells()):
        temp_face: vtkPolygon = result.GetCell(face_id)
        faceIdList.InsertNextId(temp_face.GetNumberOfPoints())
        for i in range(temp_face.GetNumberOfPoints()):
            faceIdList.InsertNextId(temp_face.GetPointId(i))

    return faceIdList

