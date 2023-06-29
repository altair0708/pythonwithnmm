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

row = 2
column = 2
point_number = column * row

for each_row in range(row):
    for each_col in range(column):

        # (0, 0, 0) - (30, 4, 47)
        x = 0 + (0.5 / (column - 1)) * each_col
        y = 0 + (0.5 / (row - 1)) * each_row
        z = 0
        special_points_coordinate.InsertNextPoint((x, y, z))

# id = 0 loading point
# id = 1 fixed point
# id = 2 measured point
point_type = vtkIntArray()
point_type.SetName('point_type')
[point_type.InsertValue(i, 1) for i in range(point_number)]

# fixed point: velocity
point_velocity = vtkDoubleArray()
point_velocity.SetName('velocity')
point_velocity.SetNumberOfComponents(3)
for i in range(point_number):
    point_velocity.InsertNextTuple((0, 0, 0))

# loading point: loading force
point_force = vtkDoubleArray()
point_force.SetName('force')
point_force.SetNumberOfComponents(3)
[point_force.InsertTuple(i, (0, 0, 0)) for i in range(point_number)]

point_displacement = vtkDoubleArray()
point_displacement.SetName('displacement_total')
point_displacement.SetNumberOfComponents(3)
[point_displacement.InsertTuple(i, (0, 0, 0)) for i in range(point_number)]

# Loading points
point_number = point_number + 1
# x = 30
# y = 0.25
# z = 0.25
x = 0.1
y = 0.1
z = 0.1
special_points_coordinate.InsertNextPoint((x, y, z))
point_type.InsertNextValue(0)
point_velocity.InsertNextTuple((0, 0, 0))
point_force.InsertNextTuple((10, 0, 0))
point_displacement.InsertNextTuple((0, 0, 0))

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

point_writer = vtkXMLUnstructuredGridWriter()
point_writer.SetFileName(output_path + '/special_point.vtu')
point_writer.SetInputData(special_point_grid)
point_writer.Write()


