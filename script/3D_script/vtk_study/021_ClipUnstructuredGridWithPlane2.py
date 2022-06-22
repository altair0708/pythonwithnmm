from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyhedron, vtkTriangle, vtkTetra, vtkUnstructuredGrid, VTK_POLYHEDRON
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints

points = vtkPoints()
points.InsertPoint(0, (0, 0, 0))
points.InsertPoint(1, (1, 0, 0))
points.InsertPoint(2, (0, 1, 0))
points.InsertPoint(3, (0, 0, 1))
points.InsertPoint(4, (-1, 0, 0))
points.InsertPoint(5, (0, -1, 0))
points.InsertPoint(6, (0, 0, -1))
u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)


def GenerateTetrahedron(order):
    tetrahedron = vtkTetra()
    tetrahedron.GetPointIds().SetId(0, order[0])
    tetrahedron.GetPointIds().SetId(1, order[1])
    tetrahedron.GetPointIds().SetId(2, order[2])
    tetrahedron.GetPointIds().SetId(3, order[3])

    face_id_list = vtkIdList()
    face_id_list.InsertNextId(4)
    for i in range(4):
        face_id_list.InsertNextId(3)
        temp_triangle: vtkTriangle = tetrahedron.GetFace(i)
        for j in range(temp_triangle.GetNumberOfPoints()):
            face_id_list.InsertNextId(temp_triangle.GetPointIds().GetId(j))
    u_grid.InsertNextCell(VTK_POLYHEDRON, face_id_list)
GenerateTetrahedron((0, 1, 2, 3))
GenerateTetrahedron((0, 1, 2, 6))
GenerateTetrahedron((0, 1, 5, 3))
GenerateTetrahedron((0, 1, 5, 6))
GenerateTetrahedron((0, 4, 2, 3))
GenerateTetrahedron((0, 4, 2, 6))
GenerateTetrahedron((0, 4, 5, 3))
GenerateTetrahedron((0, 4, 5, 6))

clipPlane1 = vtkPlane()
clipPlane1.SetOrigin(0, 0, 0)
clipPlane1.SetNormal(-1, 1, 0)

clipper1 = vtkClipDataSet()
clipper1.SetClipFunction(clipPlane1)
clipper1.SetInputData(u_grid)
clipper1.SetValue(0.0)
clipper1.GenerateClippedOutputOn()

clipPlane2 = vtkPlane()
clipPlane2.SetOrigin(0, 0, 0.5)
clipPlane2.SetNormal(0, 0, -1)

clipper2 = vtkClipDataSet()
clipper2.SetClipFunction(clipPlane2)
clipper2.SetInputConnection(clipper1.GetOutputPort())
clipper2.SetValue(0.0)
clipper2.GenerateClippedOutputOn()
clipper2.Update()

clipPlane3 = vtkPlane()
clipPlane3.SetOrigin(0, 0, 0)
clipPlane3.SetNormal(0, -1, 1)

clipper3 = vtkClipDataSet()
clipper3.SetClipFunction(clipPlane3)
clipper3.SetInputConnection(clipper2.GetOutputPort())
clipper3.SetValue(0.0)
clipper3.GenerateClippedOutputOn()
clipper3.Update()
result: vtkUnstructuredGrid = clipper3.GetOutput()

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('re021_1.vtu')
element_writer.SetInputData(result)
element_writer.Write()

element_writer = vtkXMLUnstructuredGridWriter()
element_writer.SetFileName('re021_2.vtu')
element_writer.SetInputData(u_grid)
element_writer.Write()
