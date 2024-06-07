from NMM.base.VTKBase.generate_cover_grid.generate_point_grid import generate_point_grid
from NMM.base.VTKBase.generate_cover_grid.generate_wrapped_grid import generate_wrapped_grid
from NMM.base.VTKBase.get_grid_by_cell_type import get_grid_by_cell_type
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def generate_cover_grid(vtk_model: vtkUnstructuredGrid, cover_name: str):
    if 'mathematics_cover' == cover_name:
        return generate_wrapped_grid(vtk_model)
    elif 'mathematics_point' == cover_name:
        return generate_point_grid(vtk_model)
    elif 'manifold_element' == cover_name:
        return get_grid_by_cell_type(vtk_model, 'geometric_tetrahedron')
    else:
        raise Exception('Cover name error!!!')

