from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyhedron, vtkTriangle, vtkTetra, vtkUnstructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
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
points.InsertPoint(1, (1, 0, 0))
points.InsertPoint(2, (0, 1, 0))
points.InsertPoint(3, (0, 0, 1))

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polyhedron.GetCellType(), face_id_list)

clipPlane = vtkPlane()
clipPlane.SetOrigin(0, 0, 0)
clipPlane.SetNormal(-1, 1, 0)

clipper = vtkClipDataSet()
clipper.SetClipFunction(clipPlane)
clipper.SetInputData(u_grid)
clipper.SetValue(0.0)
clipper.GenerateClippedOutputOn()
clipper.Update()
result = clipper.GetOutput()

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('re022_clipped_element.vtu')
element_writer.SetInputData(result)
element_writer.Write()

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('re022_clipper_element.vtu')
element_writer.SetInputData(u_grid)
element_writer.Write()
