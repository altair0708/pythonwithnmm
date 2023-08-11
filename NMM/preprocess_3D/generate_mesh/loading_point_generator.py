from vtkmodules.vtkCommonDataModel import vtkVertex, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray, vtkDoubleArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
import os
import numpy as np

output_path = '../../../data_3D/mesh/'
output_path = os.path.abspath(output_path)
# start point
# start_point = (0.01, 0.01, 0.01)

special_points_coordinate = vtkPoints()

# Fixed point
tol = 0.01
start_point = (0, 0, 0)

row = 5
column = 5
point_number = row * column
for each_row in range(row):
    for each_col in range(column):
        x_0 = 0
        y_0 = 0 + (0.5 / (column - 1)) * each_col
        z_0 = 0 + (0.5 / (row - 1)) * each_row
        special_points_coordinate.InsertNextPoint((x_0, y_0, z_0))

# (0, 0, 0), (1, 0, 0), (0, 1, 0)
# x = 0
# y = 0
# z = 0
# x0 = 1
# y0 = 0
# z0 = 0
# x1 = 0
# y1 = 1
# z1 = 0
# point_number = 3
# special_points_coordinate.InsertNextPoint((x, y, z))
# special_points_coordinate.InsertNextPoint((x0, y0, z0))
# special_points_coordinate.InsertNextPoint((x1, y1, z1))

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
for i in range(point_number):
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

# Loading points
point_number = point_number + 1
x = 30
y = 0.25
z = 0.25
# x = 0
# y = 0
# z = 1
special_points_coordinate.InsertNextPoint((x, y, z))
point_type.InsertNextValue(0)
point_velocity.InsertNextTuple((0, 0, 0))
point_force.InsertNextTuple((0, 0, 100))
point_displacement.InsertNextTuple((0, 0, 0))

point_group.InsertNextValue(0)
point_displacement_difference.InsertNextTuple((0, 0, 0))

# unstructured grid
special_point_grid = vtkUnstructuredGrid()
for each_point_id in range(point_number):
    temp_point = vtkVertex()
    temp_point.GetPointIds().InsertId(0, each_point_id)
    special_point_grid.InsertNextCell(temp_point.GetCellType(), temp_point.GetPointIds())

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


