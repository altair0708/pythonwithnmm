from NMM.base.VTKBase.generate_entity.get_grid_by_cell_type.get_grid_by_cell_type import get_grid_by_cell_type
from NMM.base.VTKBase.generate_entity.generate_cover_grid.generate_cover_grid import generate_cover_grid
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def generate_grid(vtk_grid: vtkUnstructuredGrid, entity_name: str):
    geometric_list = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron']
    cover_list = ['mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface']
    if entity_name in geometric_list:
        return get_grid_by_cell_type(vtk_grid, entity_name)
    elif entity_name in cover_list:
        # Id information is also generated
        return generate_cover_grid(vtk_grid, entity_name)

