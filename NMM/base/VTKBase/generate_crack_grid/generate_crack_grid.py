from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from NMM.base.VTKBase.generate_crack_grid.generate_crack_surface import generate_crack_surface
from NMM.base.VTKBase.generate_crack_grid.generate_crack_edge import generate_crack_edge


def generate_crack_grid(crack_grid: vtkUnstructuredGrid, element_grid: vtkUnstructuredGrid, crack_name: str):
    if 'crack_surface' == crack_name:
        return generate_crack_surface(crack_grid, element_grid)
    elif 'crack_edge' == crack_name:
        return generate_crack_edge(crack_grid, element_grid)
