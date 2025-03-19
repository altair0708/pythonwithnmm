from NMM.base.VTKBase import copy_cell_data, load_a_grid, write_file


def test_copy_cell_data():

    origin_grid = load_a_grid('test_grid.vtu')

    target_grid = load_a_grid('test_grid_1.vtu')

    copy_cell_data(origin_grid, target_grid, 'cell_id')

    write_file(target_grid, 'test_grid_2.vtu')

