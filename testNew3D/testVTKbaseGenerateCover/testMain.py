from NMM.base.VTKBase import generate_grid, load_a_grid, new_a_grid
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def test_generate_cover():
    vtk_model: vtkUnstructuredGrid = load_a_grid('geometric_tetrahedron.vtu')
    element: vtkUnstructuredGrid = generate_grid(vtk_model, 'manifold_element')
    cover: vtkUnstructuredGrid = generate_grid(vtk_model, 'mathematics_cover')
    cover_point: vtkUnstructuredGrid = generate_grid(vtk_model, 'mathematics_point')

    assert cover.GetNumberOfCells() == element.GetNumberOfPoints() == cover_point.GetNumberOfCells()
    assert cover_point.GetNumberOfPoints() == cover_point.GetNumberOfCells()
    assert cover.GetCellData().GetNumberOfArrays() == cover_point.GetCellData().GetNumberOfArrays()
    assert cover.GetCellData().GetArrayName(0) == 'cell_id'
    assert cover_point.GetCellData().GetArrayName(0) == 'cell_id'
    assert cover.GetCellData().GetArray(0).GetNumberOfTuples() == vtk_model.GetNumberOfPoints()

    for each_id in range(vtk_model.GetNumberOfPoints()):
        assert cover.GetCellData().GetArray(0).GetTuple(each_id) == vtk_model.GetPointData().GetArray(0).GetTuple(each_id)
        assert cover_point.GetCellData().GetArray(0).GetTuple(each_id) == vtk_model.GetPointData().GetArray(0).GetTuple(each_id)
        assert element.GetCellData().GetArray(0).GetTuple(each_id) == vtk_model.GetCellData().GetArray(0).GetTuple(each_id)

