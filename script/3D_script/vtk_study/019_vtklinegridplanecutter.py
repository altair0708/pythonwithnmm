from vtkmodules.vtkFiltersCore import vtk3DLinearGridPlaneCutter, vtkPlaneCutter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLPolyDataWriter, vtkXMLUnstructuredGridReader
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra, vtkPlane, vtkPolyData, vtkPolyhedron, vtkTriangle, vtkPartitionedDataSet, vtkPolygon
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList

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
points.InsertPoint(1, (1, 0, 0))
points.InsertPoint(2, (0, 1, 0))
points.InsertPoint(3, (0, 0, 1))

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polyhedron.GetCellType(), face_id_list)
# u_grid.InsertNextCell(tetrahedron.GetCellType(), tetrahedron.GetPointIds())

grid_reader = vtkXMLUnstructuredGridReader()
grid_reader.SetFileName('temp_math_cover.vtu')
grid_reader.Update()

cutter_plane = vtkPlane()
cutter_plane.SetNormal(1, -1, 0)
cutter_plane.SetOrigin(0, 0, 1)

# cutter = vtk3DLinearGridPlaneCutter()
cutter = vtkPlaneCutter()
cutter.SetPlane(cutter_plane)
cutter.SetInputConnection(grid_reader.GetOutputPort())
cutter.GeneratePolygonsOff()
# cutter.SetInputData(u_grid)
cutter.Update()

result: vtkPartitionedDataSet = cutter.GetOutput()
result: vtkPolyData = result.GetPartition(0)
temp_cell: vtkPolygon = result.GetCell(0)
print(temp_cell.GetPoints())

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('cutter_element.vtu')
element_writer.SetInputData(u_grid)
element_writer.Write()

polydata_writer = vtkXMLPolyDataWriter()
polydata_writer.SetFileName('cutter_polydata.vtp')
polydata_writer.SetInputData(result)
polydata_writer.Write()
