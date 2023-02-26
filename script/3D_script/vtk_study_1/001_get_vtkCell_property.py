from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.control_3D.ElementRefresh3D import get_property, set_property

path = '../../../data_3D/geometry/manifold_element.vtu'

vtk_model = ElementIOer3D.load_vtk_model(path)
result = get_property(vtk_model, 'point_displacement_total', 0)
print(result)
set_property(vtk_model, 'point_displacement_total', 0, (1, 1, 1))
result = get_property(vtk_model, 'point_displacement_total', 0)
print(result)
set_property(vtk_model, 'point_displacement_total', 0, (0, 0, 0))
result = get_property(vtk_model, 'point_displacement_total', 0)
print(result)


