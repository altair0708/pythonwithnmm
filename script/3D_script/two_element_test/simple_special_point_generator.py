from vtkmodules.vtkCommonDataModel import vtkVertex, vtkUnstructuredGrid
import os
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray, vtkDoubleArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

output_path = './'
output_path = os.path.abspath(output_path)
# start point
# start_point = (0.01, 0.01, 0.01)
tol = 0.01
start_point = (0, 0, 0)

point_number = 2

special_point_grid = vtkUnstructuredGrid()
for each_point_id in range(point_number):
    temp_point = vtkVertex()
    temp_point.GetPointIds().InsertId(0, each_point_id)
    special_point_grid.InsertNextCell(temp_point.GetCellType(), temp_point.GetPointIds())

special_points_coordinate = vtkPoints()
special_points_coordinate.InsertNextPoint((0.99999, 0, 0))
special_points_coordinate.InsertNextPoint((-0.9999, 0, 0))

# id = 0 loading point
# id = 1 fixed point
# id = 2 measured point
point_type = vtkIntArray()
point_type.SetName('point_type')
[point_type.InsertValue(i, 0) for i in range(point_number)]

point_group = vtkIntArray()
point_group.SetName('group')
point_group.InsertNextValue(0)
point_group.InsertNextValue(0)

# fixed point: velocity
point_velocity = vtkDoubleArray()
point_velocity.SetName('velocity')
point_velocity.SetNumberOfComponents(3)
point_velocity.InsertNextTuple((0.0001, 0, 0))
point_velocity.InsertNextTuple((-0.0001, 0, 0))
# [point_velocity.InsertTuple(i, (i, i, i)) for i in range(6)]
# point_velocity.InsertNextTuple((0, 0, 0))

# loading point: loading force
point_force = vtkDoubleArray()
point_force.SetName('force')
point_force.SetNumberOfComponents(3)
point_force.InsertNextTuple((100, 0, 0))
point_force.InsertNextTuple((-100, 0, 0))

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
point_writer.SetFileName('special_point.vtu')
point_writer.SetInputData(special_point_grid)
point_writer.Write()


