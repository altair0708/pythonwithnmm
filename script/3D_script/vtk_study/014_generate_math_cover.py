import pygmsh
from vtkmodules.vtkIOXML import (vtkXMLUnstructuredGridReader,
                                 vtkXMLUnstructuredGridWriter,
                                 vtkXMLPolyDataWriter)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           vtkPolyData,
                                           vtkPolygon,
                                           vtkCell,
                                           vtkPolyhedron,
                                           VTK_POLYHEDRON,
                                           VTK_TETRA)
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkUnsignedCharArray

with pygmsh.occ.Geometry() as geom:
    geom.add_box([0, 0, 0],
                 [1, 1, 1], mesh_size=0.1)
    mesh = geom.generate_mesh()
mesh.write('original_gmsh.vtu')

uGridReader = vtkXMLUnstructuredGridReader()
uGridReader.SetFileName('original_gmsh.vtu')
uGridReader.Update()
uGrid: vtkUnstructuredGrid = uGridReader.GetOutput()

# TODO:2.get number of tetrahedron
# TODO:step1.get all tetrahedron from uGrid
cellType = VTK_TETRA
print(type(VTK_TETRA))

tetraGrid = vtkUnstructuredGrid()
cellNumber = uGrid.GetNumberOfCells()

for cellId in range(cellNumber):
    if uGrid.GetCellType(cellId) == cellType:
        tempCell: vtkCell = uGrid.GetCell(cellId)
        tetraGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
tetraGrid.SetPoints(uGrid.GetPoints())

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('cell.vtu')
writer.SetInputData(tetraGrid)
writer.Write()

# Get CellId from UnstructuredGrid by selected point
mathCover = vtkUnstructuredGrid()
print('number of points: {}'.format(tetraGrid.GetNumberOfPoints()))
print('number of cells: {}'.format(tetraGrid.GetNumberOfCells()))
for each_id in range(tetraGrid.GetNumberOfPoints()):
    cellIdList = vtkIdList()
    pointId = each_id
    tetraGrid.GetPointCells(pointId, cellIdList)

    # Generate new grid of selected cell
    mathGrid = vtkUnstructuredGrid()
    idNumber = cellIdList.GetNumberOfIds()
    for eachId in range(idNumber):
        cellId = cellIdList.GetId(eachId)
        tempCell: vtkCell = tetraGrid.GetCell(cellId)
        mathGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
    mathGrid.SetPoints(uGrid.GetPoints())

    # TODO: Generate math cover polyhedron by polygon
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
    print(each_id)

mathCover.SetPoints(tetraGrid.GetPoints())
mathWriter = vtkXMLUnstructuredGridWriter()
mathWriter.SetFileName('math_cover.vtu')
mathWriter.SetInputData(mathCover)
mathWriter.Write()

mathReader = vtkXMLUnstructuredGridReader()
mathReader.SetFileName('../../../data_3D/math_cover.vtu')
mathReader.Update()
mathCover1: vtkUnstructuredGrid = mathReader.GetOutput()
temp_cell = vtkIdList()
mathCover1.GetFaceStream(40, temp_cell)
temp_grid = vtkUnstructuredGrid()
temp_grid.InsertNextCell(VTK_POLYHEDRON, temp_cell)
temp_grid.SetPoints(mathCover1.GetPoints())

mathWriter = vtkXMLUnstructuredGridWriter()
mathWriter.SetFileName('temp_grid.vtu')
mathWriter.SetInputData(temp_grid)
mathWriter.Write()
