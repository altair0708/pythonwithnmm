def test_find_close_cell():
    from NMM.base.VTKBase import (find_close_cell,
                                  generate_point_grid,
                                  load_a_grid,
                                  debug_write_file,
                                  generate_tetra_polyhedron,
                                  new_a_grid,
                                  insert_a_vtk_cell)
    from NMM.base.Property.Implement.VtkGrid import VtkGrid

    point_grid = generate_point_grid()
    _, _, _, tetra = generate_tetra_polyhedron()
    vtk_model = new_a_grid()
    insert_a_vtk_cell(tetra, vtk_model)
    print(find_close_cell(point_grid, vtk_model))
    print(find_close_cell(point_grid, tetra))

    # vtk_model = VtkGrid('manifold_element', 'manifold_element.vtu')
    # point_grid = VtkGrid('special_point', 'special_point.vtu')
    # for each_point in point_grid:
    #     find_close_cell(each_point, vtk_model.value)

