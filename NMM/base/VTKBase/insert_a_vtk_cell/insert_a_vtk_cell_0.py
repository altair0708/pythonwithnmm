from vtkmodules.vtkFiltersCore import vtkAppendFilter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def insert_a_vtk_cell(cell_grid: vtkUnstructuredGrid, target_grid: vtkUnstructuredGrid):
    appender = vtkAppendFilter()
    appender.SetOutputPointsPrecision(appender.DOUBLE_PRECISION)
    appender.AddInputData(cell_grid)
    appender.AddInputData(target_grid)
    appender.Update()
    return appender.GetOutput()
