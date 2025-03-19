from NMM.base.VTKBase import load_a_grid, get_cell_point_id


def test_get_cell_point_id():
    vtk_model = load_a_grid('test_grid.vtu')
    point_id = get_cell_point_id(vtk_model, 1)
    print(point_id)
