from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter


def extract_geometric_shell(vtk_model: vtkUnstructuredGrid):
    surface_filter = vtkDataSetSurfaceFilter()
    surface_filter.SetInputData(vtk_model)
    surface_filter.Update()
    return surface_filter.GetOutput()

