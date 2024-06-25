from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkIntArray
from NMM.base.VTKBase.generate_entity.generate_cover_grid.get_polyhedron_by_point import get_polyhedron_by_point
from NMM.base.VTKBase import new_a_grid


def generate_wrapped_grid(vtk_model: vtkUnstructuredGrid):
    target_grid = new_a_grid()
    target_grid.GetPoints().DeepCopy(vtk_model.GetPoints())

    # add cover id
    array = vtkIntArray()
    array.SetName('cell_id')
    array.SetNumberOfComponents(1)

    for each_point in range(vtk_model.GetNumberOfPoints()):
        face_id_list = get_polyhedron_by_point(each_point, vtk_model)
        target_grid.InsertNextCell(VTK_POLYHEDRON, face_id_list)

        array.InsertNextTuple((each_point, ))

    target_grid.GetCellData().AddArray(array)

    return target_grid
