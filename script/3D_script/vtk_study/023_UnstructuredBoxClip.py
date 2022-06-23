from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet

manifold_element = vtkUnstructuredGrid()

for x_number in range(11):
    for y_number in range(11):
        for z_number in range(11):
            temp_cube = vtkIdList()
            temp_cube.InsertNextId(6)
            for each_face in range(6):
                temp_cube.InsertNextId(4)

