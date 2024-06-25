from NMM.base.VTKBase.generate_entity.generate_cover_grid.generate_point_grid import generate_point_grid
from NMM.base.VTKBase.generate_entity.generate_cover_grid.generate_wrapped_grid import generate_wrapped_grid
from NMM.base.VTKBase.new_a_grid import new_a_grid
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


# Id information is also generated
def generate_cover_grid(vtk_model: vtkUnstructuredGrid, cover_name: str):
    if 'mathematics_cover' == cover_name:
        return generate_wrapped_grid(vtk_model)
    elif 'mathematics_point' == cover_name:
        return generate_point_grid(vtk_model)
    elif 'manifold_element' == cover_name:
        new_vtk_model = new_a_grid()
        new_vtk_model.DeepCopy(vtk_model)
        return new_vtk_model
    else:
        raise Exception('Cover name error!!!')

