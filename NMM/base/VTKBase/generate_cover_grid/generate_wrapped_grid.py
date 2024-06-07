from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON
from NMM.base.VTKBase.generate_cover_grid.get_polyhedron_by_point import get_polyhedron_by_point
from NMM.base.VTKBase import new_a_grid


def generate_wrapped_grid(vtk_model: vtkUnstructuredGrid):
    target_grid = new_a_grid()
    target_grid.GetPoints().DeepCopy(vtk_model.GetPoints())

    for each_point in range(vtk_model.GetNumberOfPoints()):
        face_id_list = get_polyhedron_by_point(each_point, vtk_model)
        target_grid.InsertNextCell(VTK_POLYHEDRON, face_id_list)

    return target_grid
