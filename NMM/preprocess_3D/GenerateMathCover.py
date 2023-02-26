from NMM.control_3D.ElementIO3D import ElementIOer3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPolyData, vtkPolygon, vtkVertex, VTK_POLYHEDRON
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkCommonCore import vtkIntArray, vtkDoubleArray, vtkIdList, vtkPoints


def generate_math_cover(mesh_path: str, geometry_path: str):
    gmshGrid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + 'geometry_tetrahedron.vtu')

    mathCover = vtkUnstructuredGrid()

    mathPointId = vtkIntArray()
    mathPointId.SetName('math_cover_id')
    mathPointId.SetNumberOfComponents(1)

    mathPointCoordinate = vtkDoubleArray()
    mathPointCoordinate.SetName('math_cover_coordinate')
    mathPointCoordinate.SetNumberOfComponents(3)

    mathPointDisplacement = vtkDoubleArray()
    mathPointDisplacement.SetName('math_cover_displacement')
    mathPointDisplacement.SetNumberOfComponents(3)

    print('original mesh info:')
    print('number of points: {}'.format(gmshGrid.GetNumberOfPoints()))
    print('number of cells: {}'.format(gmshGrid.GetNumberOfCells()))
    for each_id in range(gmshGrid.GetNumberOfPoints()):
        cellIdList = vtkIdList()
        pointId = each_id
        gmshGrid.GetPointCells(pointId, cellIdList)

        # Generate new grid of selected cell
        mathGrid = vtkUnstructuredGrid()
        idNumber = cellIdList.GetNumberOfIds()
        for eachId in range(idNumber):
            cellId = cellIdList.GetId(eachId)
            tempCell: vtkCell = gmshGrid.GetCell(cellId)
            mathGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
        mathGrid.SetPoints(gmshGrid.GetPoints())

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

        mathCover.InsertNextCell(VTK_POLYHEDRON, faceIdList)
        mathPointId.InsertValue(each_id, each_id)
        mathPointCoordinate.InsertNextTuple(gmshGrid.GetPoint(each_id))
        temp_displacement = (0, 0, 0)
        mathPointDisplacement.InsertNextTuple(temp_displacement)
        # print(mathPointCoordinate.GetTuple(each_id) == gmshGrid.GetPoint(each_id))

    mathCover.SetPoints(gmshGrid.GetPoints())
    mathCover.GetCellData().AddArray(mathPointId)
    mathCover.GetCellData().AddArray(mathPointCoordinate)
    mathCover.GetCellData().AddArray(mathPointDisplacement)

    mathWriter = vtkXMLUnstructuredGridWriter()
    outputFile = geometry_path + 'math_cover.vtu'
    mathWriter.SetFileName(outputFile)
    mathWriter.SetInputData(mathCover)
    mathWriter.Write()


def generate_math_point(mesh_path: str, geometry_path: str):
    gmshGrid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + 'geometry_tetrahedron.vtu')
    pointNumber = gmshGrid.GetNumberOfPoints()
    print('math_cover_number:{}'.format(pointNumber))
    vertexGrid = vtkUnstructuredGrid()
    for each_id in range(pointNumber):
        vertex = vtkVertex()
        vertex.GetPointIds().SetId(0, each_id)
        vertexGrid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

    mathPointDisplacement = vtkDoubleArray()
    mathPointDisplacement.SetName('math_point_displacement')
    mathPointDisplacement.SetNumberOfComponents(3)

    vertexGrid.SetPoints(gmshGrid.GetPoints())
    vertexGrid.GetPointData().AddArray(mathPointDisplacement)

    outputFile = 'math_point.vtu'
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName(geometry_path + outputFile)
    writer.SetInputData(vertexGrid)
    writer.Write()
