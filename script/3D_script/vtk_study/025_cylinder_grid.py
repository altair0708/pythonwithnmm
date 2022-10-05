from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           VTK_POLYHEDRON,
                                           vtkPolygon,
                                           vtkPlane,
                                           vtkPolyhedron)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkFiltersCore import vtkFeatureEdges
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName('re023_5.vtu')
reader.Update()
u_grid = reader.GetOutput()

points = vtkPoints()
points.InsertNextPoint(2.5, 0.5, 0.5)
points.InsertNextPoint(7.5, 0.5, 0.5)
points.InsertNextPoint(9.5, 2.5, 0.5)
points.InsertNextPoint(9.5, 7.5, 0.5)
points.InsertNextPoint(7.5, 9.5, 0.5)
points.InsertNextPoint(2.5, 9.5, 0.5)
points.InsertNextPoint(0.5, 7.5, 0.5)
points.InsertNextPoint(0.5, 2.5, 0.5)
points.InsertNextPoint(2.5, 0.5, 1.5)
points.InsertNextPoint(7.5, 0.5, 1.5)
points.InsertNextPoint(9.5, 2.5, 1.5)
points.InsertNextPoint(9.5, 7.5, 1.5)
points.InsertNextPoint(7.5, 9.5, 1.5)
points.InsertNextPoint(2.5, 9.5, 1.5)
points.InsertNextPoint(0.5, 7.5, 1.5)
points.InsertNextPoint(0.5, 2.5, 1.5) # 16 points

def generate_cylinder_list(number_of_edge):
    id_list = vtkIdList()
    number_of_face = number_of_edge + 2
    id_list.InsertNextId(number_of_face)

    for each_side in range(number_of_edge - 1):
        id_list.InsertNextId(4)
        id_list.InsertNextId(each_side)
        id_list.InsertNextId(each_side + 1)
        id_list.InsertNextId(each_side + number_of_edge + 1)
        id_list.InsertNextId(each_side + number_of_edge)

    id_list.InsertNextId(4)
    id_list.InsertNextId(number_of_edge - 1)
    id_list.InsertNextId(0)
    id_list.InsertNextId(number_of_edge)
    id_list.InsertNextId(2 * number_of_edge - 1)

    id_list.InsertNextId(number_of_edge)
    for each_id in range(number_of_edge):
        id_list.InsertNextId(each_id)

    id_list.InsertNextId(number_of_edge)
    for each_id in range(number_of_edge):
        id_list.InsertNextId(number_of_edge + each_id)
    return id_list


cylinder: vtkIdList = generate_cylinder_list(8)

cylinder_grid = vtkUnstructuredGrid()
cylinder_grid.SetPoints(points)
cylinder_grid.InsertNextCell(VTK_POLYHEDRON, cylinder)

cylinder_writer = vtkXMLUnstructuredGridWriter()
cylinder_writer.SetFileName('re025_1.vtu')
cylinder_writer.SetInputData(cylinder_grid)
cylinder_writer.Write()

solve_cell: vtkPolyhedron = cylinder_grid.GetCell(0)


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

temp_grid: vtkUnstructuredGrid = u_grid

# clipper = vtkClipDataSet()
# clipper.SetInputData(temp_grid)
# clipper.SetClipFunction(generate_plane(0))
# clipper.InsideOutOn()
# clipper.Update()
# temp_grid: vtkUnstructuredGrid = clipper.GetOutput()

clipper = vtkClipDataSet()
clipper.SetInputData(temp_grid)
clipper.SetClipFunction(generate_plane(1))
clipper.InsideOutOn()
clipper.Update()
temp_grid: vtkUnstructuredGrid = clipper.GetOutput()

clipper = vtkClipDataSet()
clipper.SetInputData(temp_grid)
clipper.SetClipFunction(generate_plane(2))
clipper.InsideOutOn()
clipper.Update()
temp_grid: vtkUnstructuredGrid = clipper.GetOutput()

print(temp_grid.GetNumberOfCells())
cylinder_writer = vtkXMLUnstructuredGridWriter()
cylinder_writer.SetFileName('re025_2.vtu')
cylinder_writer.SetInputData(temp_grid)
cylinder_writer.Write()
