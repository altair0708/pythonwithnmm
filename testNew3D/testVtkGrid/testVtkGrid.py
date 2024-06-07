from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell
from NMM.base.Property.Implement.VtkGrid import VtkGrid


def test_id_consistency():
    # initial VtkGrid
    vtk_grid = VtkGrid('gmsh_file', 'test_grid.vtu')
    vtk_grid.add_attribute('cell_id')
    vtk_grid.add_attribute('point_id')

    vtk_model: vtkUnstructuredGrid = vtk_grid.value

    # cell check
    cell_data = vtk_model.GetCellData()
    assert cell_data.GetArrayName(0) == 'cell_id'
    property_data = cell_data.GetArray(0)
    for each_id in range(vtk_model.GetNumberOfCells()):
        assert property_data.GetTuple(each_id)[0] == each_id

    # point check
    point_data = vtk_model.GetCellData()
    assert point_data .GetArrayName(0) == 'point_id'
    property_data = point_data .GetArray(0)
    for each_id in range(vtk_model.GetNumberOfCells()):
        assert property_data.GetTuple(each_id)[0] == each_id

