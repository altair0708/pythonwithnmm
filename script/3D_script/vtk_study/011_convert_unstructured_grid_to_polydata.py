import pygmsh
from vtkmodules.vtkIOXML import (vtkXMLUnstructuredGridReader,
                                 vtkXMLUnstructuredGridWriter,
                                 vtkXMLPolyDataWriter)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           vtkPolyData,
                                           vtkCellTypes,
                                           vtkPolygon,
                                           vtkCell,
                                           vtkVertex,
                                           vtkPolyhedron,
                                           vtkTetra,
                                           vtkLine,
                                           VTK_POLYHEDRON,
                                           VTK_TETRA,
                                           VTK_VERTEX,
                                           VTK_LINE,
                                           VTK_TRIANGLE)
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkUnsignedCharArray

with pygmsh.occ.Geometry() as geom:
    geom.add_box([0, 0, 0],
                 [1, 1, 1], mesh_size=0.1)
    mesh = geom.generate_mesh()
mesh.write('ugrid2polydata.vtu')

uGridReader = vtkXMLUnstructuredGridReader()
uGridReader.SetFileName('ugrid2polydata.vtu')
uGridReader.Update()

uGrid: vtkUnstructuredGrid = uGridReader.GetOutput()
# pointData: vtkPoints = uGrid.GetPoints()

# Get point list of a cell by cellId
# pointList = vtkIdList()
# uGrid.GetCellPoints(1, pointList)

# Get all cell type of unstructured grid
# cellTypes = vtkCellTypes()
# uGrid.GetCellTypes(cellTypes)


# # TODO: Get all cells use the selected point which given by pointId
# # Get CellId from UnstructuredGrid by selected point
# cellIdList = vtkIdList()
# pointId = 737
# uGrid.GetPointCells(pointId, cellIdList)
#
# # Generate new grid of selected cell
# mathGrid = vtkUnstructuredGrid()
# idNumber = cellIdList.GetNumberOfIds()
# for eachId in range(idNumber):
#     cellId = cellIdList.GetId(eachId)
#     tempCell: vtkCell = uGrid.GetCell(cellId)
#     mathGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
# mathGrid.SetPoints(uGrid.GetPoints())
#
# # Write grid to file
# writer = vtkXMLUnstructuredGridWriter()
# writer.SetFileName('math.vtu')
# writer.SetInputData(mathGrid)
# writer.Write()
#
# # Write selected point information
# pointGrid = vtkUnstructuredGrid()
# vertex = vtkVertex()
# vertex.GetPointIds().SetId(0, pointId)
# pointGrid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
# pointGrid.SetPoints(uGrid.GetPoints())
# writer.SetFileName('vertex.vtu')
# writer.SetInputData(pointGrid)
# writer.Write()

# # TODO: Get one certain type of cell from UnstructuredGrid
# cellType = VTK_TETRA
#
# vertexGrid = vtkUnstructuredGrid()
# cellNumber = uGrid.GetNumberOfCells()
#
# for cellId in range(cellNumber):
#     if uGrid.GetCellType(cellId) == cellType:
#         tempCell: vtkCell = uGrid.GetCell(cellId)
#         vertexGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
# vertexGrid.SetPoints(uGrid.GetPoints())
#
# writer = vtkXMLUnstructuredGridWriter()
# writer.SetFileName('cell.vtu')
# writer.SetInputData(vertexGrid)
# writer.Write()

# # TODO:Write math cover(polyhedron) into file math_cover.vtu, we should turn multi tetrahedron into one polyhedron
# # TODO:1.Test of polyhedron
#
# # point list of unstructured grid
# pointList = vtkPoints()
# pointList.InsertNextPoint(0, 0, 0)
# pointList.InsertNextPoint(1, 0, 0)
# pointList.InsertNextPoint(1, 1, 0)
# pointList.InsertNextPoint(0, 1, 0)
# pointList.InsertNextPoint(0, 0, 1)
# pointList.InsertNextPoint(1, 0, 1)
# pointList.InsertNextPoint(1, 1, 1)
# pointList.InsertNextPoint(0, 1, 1)
#
# # faces of polyhedron
# faceId = vtkIdList()
# faces = [[0, 3, 2, 1],
#          [0, 4, 7, 3],
#          [4, 5, 6, 7],
#          [5, 1, 2, 6],
#          [0, 1, 5, 4],
#          [2, 3, 7, 6]]
# face_1 = [6,
#           4, 0, 3, 2, 1,
#           4, 0, 4, 7, 3,
#           4, 4, 5, 6, 7,
#           4, 5, 1, 2, 6,
#           4, 0, 1, 5, 4,
#           4, 2, 3, 7, 6]
# faceId.InsertNextId(6)
# for each_face in faces:
#     faceId.InsertNextId(len(each_face))
#     [faceId.InsertNextId(i) for i in each_face]
#
# # construct the polyhedron
# polyhedron = vtkPolyhedron()
# for i in range(8):
#     polyhedron.GetPointIds().InsertNextId(i)
# polyhedron.GetPoints().InsertNextPoint(0, 0, 0)
# polyhedron.GetPoints().InsertNextPoint(1, 0, 0)
# polyhedron.GetPoints().InsertNextPoint(1, 1, 0)
# polyhedron.GetPoints().InsertNextPoint(0, 1, 0)
# polyhedron.GetPoints().InsertNextPoint(0, 0, 1)
# polyhedron.GetPoints().InsertNextPoint(1, 0, 1)
# polyhedron.GetPoints().InsertNextPoint(1, 1, 1)
# polyhedron.GetPoints().InsertNextPoint(0, 1, 1)
# polyhedron.SetFaces(face_1)
# polyhedron.Initialize()
#
# # construct tetrahedron
# temp_tetra = vtkTetra()
# temp_tetra.GetPointIds().SetId(0, 0)
# temp_tetra.GetPointIds().SetId(1, 1)
# temp_tetra.GetPointIds().SetId(2, 3)
# temp_tetra.GetPointIds().SetId(3, 4)
#
# # construct the unstructured grid of polyhedron
# polyGrid = vtkUnstructuredGrid()
# # polyGrid.InsertNextCell(temp_tetra.GetCellType(), temp_tetra.GetPointIds())
# polyGrid.InsertNextCell(polyhedron.GetCellType(), faceId)
# polyGrid.SetPoints(pointList)
# print(polyhedron.GetFaces())
# print(type(polyhedron.GetFaces()))
#
# # get polyhedron from ugrid
# temp_points = vtkIdList()
# polyGrid.GetFaceStream(0, temp_points)
# temp_polyhedron: vtkTetra = polyGrid.GetCell(0)
#
# # writer = vtkXMLUnstructuredGridWriter()
# writer = vtkXMLUnstructuredGridWriter()
# writer.SetFileName('polyhedron.vtu')
# writer.SetInputData(uGrid)
# writer.Write()

''''''
# TODO:2.get number of tetrahedron
# TODO:step1.get all tetrahedron from uGrid
cellType = VTK_TETRA

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
cellIdList = vtkIdList()
pointId = 737
tetraGrid.GetPointCells(pointId, cellIdList)

# Generate new grid of selected cell
mathGrid = vtkUnstructuredGrid()
idNumber = cellIdList.GetNumberOfIds()
for eachId in range(idNumber):
    cellId = cellIdList.GetId(eachId)
    tempCell: vtkCell = tetraGrid.GetCell(cellId)
    mathGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
mathGrid.SetPoints(uGrid.GetPoints())

# # TODO: Generate math cover polyhedron
# mathPolyhedronGrid = vtkUnstructuredGrid()
# mathTetrahedronNumber = mathGrid.GetNumberOfCells()
# print('number of tetrahedrons: {}'.format(mathTetrahedronNumber))
# i = 0
# temp_face = []
# polyhedronPointIdList = vtkIdList()
# for each_cell_id in range(mathTetrahedronNumber):
#     temp_cell: vtkTetra = mathGrid.GetCell(each_cell_id)
#     temp_plane_number = temp_cell.GetNumberOfFaces()
#     for each_plane_id in range(temp_plane_number):
#         temp_plane: vtkPolygon = temp_cell.GetFace(each_plane_id)
#
#         def IsContainSelectedPoint(select_plane: vtkPolygon):
#             temp_points: vtkIdList = select_plane.GetPointIds()
#             for j in range(3):
#                 if temp_points.GetId(j) == pointId:
#                     return True
#             return False
#
#         temp_plane_point_id = []
#         if not IsContainSelectedPoint(temp_plane):
#             i += 1
#             for k in range(3):
#                 temp_plane_point_id.append(temp_plane.GetPointId(k))
#             temp_face.append(temp_plane_point_id)
#
# faceId = vtkIdList()
# faceId.InsertNextId(i)
# for face in temp_face:
#     faceId.InsertNextId(len(face))
#     [faceId.InsertNextId(temp) for temp in face]
#
# mathPolyhedronGrid.InsertNextCell(VTK_POLYHEDRON, faceId)
# mathPolyhedronGrid.SetPoints(uGrid.GetPoints())
#
# uGridWriter = vtkXMLUnstructuredGridWriter()
# uGridWriter.SetInputData(mathPolyhedronGrid)
# uGridWriter.SetFileName('mathpolyhedron.vtu')
# uGridWriter.Write()
# print('number of planes: {}'.format(i))
# print(temp_face)

''''''
# TODO: Generate math cover polyhedron by polygon
surface = vtkGeometryFilter()
surface.PassThroughPointIdsOn()
surface.SetInputData(mathGrid)
surface.Update()
result: vtkPolyData = surface.GetOutput()

surfacePolyhedron = vtkPolyhedron()
faceIdList = vtkIdList()
faceIdList.InsertNextId(result.GetNumberOfCells())
for face_id in range(result.GetNumberOfCells()):
    temp_face: vtkPolygon = result.GetCell(face_id)
    faceIdList.InsertNextId(temp_face.GetNumberOfPoints())
    for i in range(temp_face.GetNumberOfPoints()):
        faceIdList.InsertNextId(temp_face.GetPointId(i))

mathCover = vtkUnstructuredGrid()
mathCover.InsertNextCell(VTK_POLYHEDRON, faceIdList)
mathCover.SetPoints(result.GetPoints())
mathWriter = vtkXMLUnstructuredGridWriter()
mathWriter.SetFileName('surface.vtu')
mathWriter.SetInputData(mathCover)
mathWriter.Write()

vtpWriter = vtkXMLPolyDataWriter()
vtpWriter.SetInputData(result)
vtpWriter.SetFileName('surface.vtp')
vtpWriter.Write()

