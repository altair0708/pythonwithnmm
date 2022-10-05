from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           vtkPolyhedron,
                                           vtkPolyData,
                                           vtkPolygon,
                                           vtkPlane,
                                           vtkTetra,
                                           VTK_POLYHEDRON)
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkFloatArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance
from vtkmodules.vtkCommonDataModel import vtkImplicitDataSet
from itertools import combinations

point_0 = (0.5, 0.5, 0.5)
point_1 = (0.5, 9.5, 0.5)
point_2 = (9.5, 9.5, 0.5)
point_3 = (9.5, 0.5, 0.5)
point_4 = (5, 5, 9.5)

points = vtkPoints()
points.InsertNextPoint(point_0)
points.InsertNextPoint(point_1)
points.InsertNextPoint(point_2)
points.InsertNextPoint(point_3)
points.InsertNextPoint(point_4)

polyhedron_list = vtkIdList()
polyhedron_list.InsertNextId(5)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(4)
polyhedron_list.InsertNextId(0)
polyhedron_list.InsertNextId(1)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(4)
polyhedron_list.InsertNextId(1)
polyhedron_list.InsertNextId(2)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(4)
polyhedron_list.InsertNextId(2)
polyhedron_list.InsertNextId(3)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(4)
polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(0)

polyhedron_list.InsertNextId(4)
polyhedron_list.InsertNextId(0)
polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(2)
polyhedron_list.InsertNextId(1)

u_grid = vtkUnstructuredGrid()
u_grid.InsertNextCell(VTK_POLYHEDRON, polyhedron_list)
u_grid.SetPoints(points)

u_writer = vtkXMLUnstructuredGridWriter()
u_writer.SetInputData(u_grid)
u_writer.SetFileName('re024_1.vtu')
u_writer.Write()

element_reader = vtkXMLUnstructuredGridReader()
element_reader.SetFileName('re023_3.vtu')
element_reader.Update()
element_grid: vtkUnstructuredGrid = element_reader.GetOutput()

solve_cell: vtkPolyhedron = u_grid.GetCell(0)
new_element_grid = vtkUnstructuredGrid()
element_number = element_grid.GetNumberOfCells()
for each_id in range(element_number):
    temp_cell = element_grid.GetCell(each_id)
    if solve_cell.IntersectWithCell(temp_cell):
        new_element_grid.InsertNextCell(temp_cell.GetCellType(), temp_cell.GetPointIds())
new_element_grid.SetPoints(element_grid.GetPoints())
new_element_writer = vtkXMLUnstructuredGridWriter()
new_element_writer.SetFileName('re024_2.vtu')
new_element_writer.SetInputData(new_element_grid)
new_element_writer.Write()

# turn tetra to polyhedron
tetra_polyhedron_grid = vtkUnstructuredGrid()
element_number = new_element_grid.GetNumberOfCells()
temp_tetra: vtkTetra = new_element_grid.GetCell(0)

for element_id in range(element_number):
    temp_tetra: vtkTetra = new_element_grid.GetCell(element_id)
    temp_vtk_list: vtkIdList = temp_tetra.GetPointIds()
    temp_list = []
    if temp_tetra.GetNumberOfPoints() != 4:
        raise Exception('Element point number error!')
    for i in range(temp_tetra.GetNumberOfPoints()):
        temp_list.append(temp_vtk_list.GetId(i))
    temp_face_list = combinations(temp_list, 3)
    temp_vtk_list = vtkIdList()
    temp_vtk_list.InsertNextId(4)
    for each_face in temp_face_list:
        temp_vtk_list.InsertNextId(3)
        for each_point in each_face:
            temp_vtk_list.InsertNextId(each_point)
    if temp_vtk_list.GetNumberOfIds() != 17:
        raise Exception('ID list number error!')
    tetra_polyhedron_grid.InsertNextCell(VTK_POLYHEDRON, temp_vtk_list)
tetra_polyhedron_grid.SetPoints(element_grid.GetPoints())
tetra_polyhedron_writer = vtkXMLUnstructuredGridWriter()
tetra_polyhedron_writer.SetFileName('re024_3.vtu')
tetra_polyhedron_writer.SetInputData(tetra_polyhedron_grid)
tetra_polyhedron_writer.Write()

# get planes of solve region
temp_grid = tetra_polyhedron_grid

def generate_plane(plane_id):
    temp_face: vtkPolygon = solve_cell.GetFace(plane_id)
    temp_point_list: vtkPoints = temp_face.GetPoints()
    temp_point_1 = [0, 1, 2]
    temp_point_2 = [0, 0, 0]
    temp_face.ComputeNormal(temp_point_list, 3, temp_point_1, temp_point_2)
    temp_plane = vtkPlane()
    temp_plane.SetNormal(*temp_point_2)
    temp_plane.SetOrigin(*temp_point_list.GetPoint(0))
    return temp_plane

clipper1 = vtkClipDataSet()
clipper1.SetClipFunction(generate_plane(0))
clipper1.SetInputData(temp_grid)

clipper2 = vtkClipDataSet()
clipper2.SetClipFunction(generate_plane(1))
clipper2.SetInputConnection(clipper1.GetOutputPort())

clipper3 = vtkClipDataSet()
clipper3.SetClipFunction(generate_plane(2))
clipper3.SetInputConnection(clipper2.GetOutputPort())

clipper4 = vtkClipDataSet()
clipper4.SetClipFunction(generate_plane(3))
clipper4.SetInputConnection(clipper3.GetOutputPort())

clipper5 = vtkClipDataSet()
clipper5.SetClipFunction(generate_plane(4))
clipper5.SetInputConnection(clipper4.GetOutputPort())
clipper5.Update()
result = clipper5.GetOutput()


# # clip using vtkImplicitDataSet
#
# temp_grid = element_grid
# temp_implicit_function = vtkImplicitPolyDataDistance()
# temp_polydata: vtkPolyData = solve_cell.GetPolyData()
# temp_implicit_function.SetInput(temp_polydata)
#
# signed_distances = vtkFloatArray()
# signed_distances.SetNumberOfComponents(1)
# signed_distances.SetName('SignedDistance')
#
# print(temp_grid.GetNumberOfCells())
# for point_id in range(temp_grid.GetNumberOfPoints()):
#     temp_point = temp_grid.GetPoint(point_id)
#     signed_distance = temp_implicit_function.EvaluateFunction(temp_point)
#     signed_distances.InsertNextValue(signed_distance)
#
# temp_grid.GetPointData().SetScalars(signed_distances)
#
# clipper5 = vtkClipDataSet()
# clipper5.SetInputData(temp_grid)
# clipper5.SetValue(0.0)
# clipper5.GenerateClippedOutputOn()
# clipper5.Update()
# result: vtkUnstructuredGrid = clipper5.GetOutput()
# print(result.GetNumberOfCells())

clipper_writer = vtkXMLUnstructuredGridWriter()
clipper_writer.SetFileName('re024_4.vtu')
clipper_writer.SetInputData(result)
clipper_writer.Write()
