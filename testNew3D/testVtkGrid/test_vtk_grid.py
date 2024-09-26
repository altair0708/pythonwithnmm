from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell
from vtkmodules.vtkCommonCore import vtkIdList
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase import is_vtk_grid


def test_id_consistency():
    # initial VtkGrid
    vtk_grid = VtkGrid('test_1', 'geometric_tetrahedron.vtu')
    vtk_grid.add_attribute('cell_id')
    vtk_grid.add_attribute('point_id')

    vtk_model: vtkUnstructuredGrid = vtk_grid.value

    # cell check
    cell_data = vtk_model.GetCellData()
    assert cell_data.GetArrayName(0) == 'cell_id'
    property_data = cell_data.GetArray(0)
    for each_id in range(vtk_model.GetNumberOfCells()):
        assert property_data.GetTuple(each_id)[0] == each_id
        # In geometric_tetrahedron.vtu each cell have four vertices
        id_list = vtkIdList()
        vtk_model.GetCellPoints(each_id, id_list)
        assert id_list.GetNumberOfIds() == 4

    # point check
    point_data = vtk_model.GetPointData()
    assert point_data.GetArrayName(0) == 'point_id'
    property_data = point_data.GetArray(0)
    for each_id in range(vtk_model.GetNumberOfPoints()):
        assert property_data.GetTuple(each_id)[0] == each_id


def test_is_vtk_grid():
    vtk_grid = VtkGrid('test_2', 'geometric_tetrahedron.vtu')
    vtk_grid.add_attribute('cell_id')
    vtk_grid.add_attribute('point_id')

    vtk_model: vtkUnstructuredGrid = vtk_grid.value
    print(type(vtk_model))
    print(vtkUnstructuredGrid)
    print(type(vtk_model) == vtkUnstructuredGrid)
    print(type(vtk_model) is vtkUnstructuredGrid)


def test_iterator():
    vtk_grid = VtkGrid('test_3', 'geometric_tetrahedron.vtu')
    vtk_grid.add_attribute('cell_id')
    vtk_grid.add_attribute('point_id')
    for i in vtk_grid:
        print(i.GetNumberOfPoints())




