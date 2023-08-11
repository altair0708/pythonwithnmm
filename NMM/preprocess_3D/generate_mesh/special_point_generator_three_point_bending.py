from vtkmodules.vtkCommonDataModel import vtkVertex, vtkUnstructuredGrid
import os
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray, vtkDoubleArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

output_path = '../../../data_3D/mesh/'
output_path = os.path.abspath(output_path)
# start point
# start_point = (0.01, 0.01, 0.01)
tol = 0.01
start_point = (0, 0, 0)

row = 61
point_number = row * 3

special_point_grid = vtkUnstructuredGrid()
for each_point_id in range(point_number):
    temp_point = vtkVertex()
    temp_point.GetPointIds().InsertId(0, each_point_id)
    special_point_grid.InsertNextCell(temp_point.GetCellType(), temp_point.GetPointIds())

special_points_coordinate = vtkPoints()
for each_row in range(row):
    x = 0 + tol + ((1 - tol) / (row - 1)) * each_row

    y0 = 1
    y1 = 5.001
    y2 = 9

    z0 = 0 + tol
    z1 = 2 - tol
    z2 = 0 + tol
    special_points_coordinate.InsertNextPoint((x, y0, z0))
    special_points_coordinate.InsertNextPoint((x, y1, z1))
    special_points_coordinate.InsertNextPoint((x, y2, z2))

# id = 0 loading point
# id = 1 fixed point
# id = 2 measured point
point_type = vtkIntArray()
point_type.SetName('point_type')
[point_type.InsertValue(i, 1) for i in range(point_number)]

# point group
point_group = vtkIntArray()
point_group.SetName('group')

# fixed point: velocity
point_velocity = vtkDoubleArray()
point_velocity.SetName('velocity')
point_velocity.SetNumberOfComponents(3)
# [point_velocity.InsertTuple(i, (i, i, i)) for i in range(6)]

temp = int(point_number / 3)
for i in range(temp):
    point_velocity.InsertNextTuple((0, 0, 0))
    point_group.InsertNextValue(0)

    point_velocity.InsertNextTuple((0, 0, -0.0001))
    point_group.InsertNextValue(1)

    point_velocity.InsertNextTuple((0, 0, 0))
    point_group.InsertNextValue(0)

# loading point: loading force
point_force = vtkDoubleArray()
point_force.SetName('force')
point_force.SetNumberOfComponents(3)
[point_force.InsertTuple(i, (0, 0, 0)) for i in range(point_number)]

point_displacement = vtkDoubleArray()
point_displacement.SetName('displacement_total')
point_displacement.SetNumberOfComponents(3)
[point_displacement.InsertTuple(i, (0, 0, 0)) for i in range(point_number)]

point_displacement_difference = vtkDoubleArray()
point_displacement_difference.SetName('displacement_difference')
point_displacement_difference.SetNumberOfComponents(3)
[point_displacement_difference.InsertTuple(i, (0, 0, 0)) for i in range(point_number)]

special_point_grid.SetPoints(special_points_coordinate)
special_point_grid.GetCellData().AddArray(point_type)
special_point_grid.GetCellData().AddArray(point_velocity)
special_point_grid.GetCellData().AddArray(point_force)
special_point_grid.GetCellData().AddArray(point_displacement)

special_point_grid.GetCellData().AddArray(point_group)
special_point_grid.GetCellData().AddArray(point_displacement_difference)

point_writer = vtkXMLUnstructuredGridWriter()
point_writer.SetFileName(output_path + '/special_point.vtu')
point_writer.SetInputData(special_point_grid)
point_writer.Write()


