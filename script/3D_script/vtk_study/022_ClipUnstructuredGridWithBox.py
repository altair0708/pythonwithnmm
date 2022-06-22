from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyhedron, vtkTriangle, vtkTetra, vtkUnstructuredGrid, vtkPolygon, vtkPolyData, VTK_POLYHEDRON
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkFiltersGeneral import vtkBoxClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints

tetrahedron = vtkTetra()
tetrahedron.GetPointIds().SetId(0, 0)
tetrahedron.GetPointIds().SetId(1, 1)
tetrahedron.GetPointIds().SetId(2, 2)
tetrahedron.GetPointIds().SetId(3, 3)

polyhedron = vtkPolyhedron()
face_id_list = vtkIdList()
face_id_list.InsertNextId(4)
for i in range(4):
    face_id_list.InsertNextId(3)
    temp_triangle: vtkTriangle = tetrahedron.GetFace(i)
    for j in range(temp_triangle.GetNumberOfPoints()):
        face_id_list.InsertNextId(temp_triangle.GetPointIds().GetId(j))

points = vtkPoints()
points.InsertPoint(0, (0, 0, 0))
points.InsertPoint(1, (2, 0, 0))
points.InsertPoint(2, (0, 2, 0))
points.InsertPoint(3, (0, 0, 2))

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polyhedron.GetCellType(), face_id_list)
# u_grid.InsertNextCell(tetrahedron.GetCellType(), tetrahedron.GetPointIds())

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName('cylinder.vtu')
reader.Update()
u_grid: vtkUnstructuredGrid = reader.GetOutput()

clipper = vtkBoxClipDataSet()
clipper.SetOrientation(0)
clipper.SetBoxClip(0, 10, 0, 10, 0, 10)
# clipper.SetInputConnection(cylinder.GetOutputPort())
clipper.SetInputData(u_grid)
clipper.GenerateClippedOutputOn()
clipper.Update()
result: vtkUnstructuredGrid = clipper.GetOutput()
print(result.GetNumberOfCells())

element_cover = vtkUnstructuredGrid()

surface = vtkGeometryFilter()
surface.PassThroughPointIdsOn()
surface.SetInputData(result)
surface.MergingOff()
surface.Update()
result_1: vtkPolyData = surface.GetOutput()

faceIdList = vtkIdList()
faceIdList.InsertNextId(result_1.GetNumberOfCells())
for face_id in range(result_1.GetNumberOfCells()):
    temp_face: vtkPolygon = result_1.GetCell(face_id)
    faceIdList.InsertNextId(temp_face.GetNumberOfPoints())
    for i in range(temp_face.GetNumberOfPoints()):
        faceIdList.InsertNextId(temp_face.GetPointId(i))

element_cover.InsertNextCell(VTK_POLYHEDRON, faceIdList)

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('re022_1.vtu')
element_writer.SetInputData(result)
element_writer.Write()

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('re022_2.vtu')
element_writer.SetInputData(element_cover)
element_writer.Write()

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('re022_3.vtu')
element_writer.SetInputData(u_grid)
element_writer.Write()
