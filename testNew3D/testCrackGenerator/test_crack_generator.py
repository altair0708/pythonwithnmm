from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell import insert_a_vtk_cell
from NMM.base.VTKBase import new_a_grid, get_a_vtk_cell_grid, load_a_grid, write_file
from NMM.base.VTKBase.generate_crack_grid.generate_crack_grid import generate_crack_grid
from NMM.base.VTKBase.generate_crack_grid.clip_a_element.clip_a_element import clip_a_element


def test_insert_a_vtk_cell():
    origin_grid = load_a_grid('geometric_tetrahedron.vtu')
    new_grid = new_a_grid(allow_duplicate=False)
    # new_grid = new_a_grid()

    for each_cell in range(origin_grid.GetNumberOfCells()):
        # vtk_cell = get_a_vtk_cell_grid(origin_grid, each_cell)
        vtk_cell = get_a_vtk_cell_grid(origin_grid, each_cell, turn_polyhedron=True)
        insert_a_vtk_cell(vtk_cell, new_grid)
        # print(new_grid.GetNumberOfCells())
        # print(new_grid.GetNumberOfPoints())

    write_file(new_grid, 'test_grid.vtu')


def test_clip_surface():
    origin_grid = load_a_grid('element_surface.vtu')
    new_grid = new_a_grid(allow_duplicate=False)
    # new_grid = new_a_grid()

    for each_cell in range(origin_grid.GetNumberOfCells()):
        # vtk_cell = get_a_vtk_cell_grid(origin_grid, each_cell)
        vtk_cell = get_a_vtk_cell_grid(origin_grid, each_cell)
        insert_a_vtk_cell(vtk_cell, new_grid)
        print(new_grid.GetNumberOfCells())
        print(new_grid.GetNumberOfPoints())

    write_file(new_grid, 'test_grid.vtu')

def test_clip_a_element():
    pass


def test_generate_crack_grid():
    manifold_element = load_a_grid('geometric_tetrahedron.vtu')
    element_surface = load_a_grid('element_surface.vtu')
    initial_crack = load_a_grid('initial_crack.vtu')

    crack_surface_grid = generate_crack_grid(initial_crack, manifold_element, 'crack_surface')
    crack_edge_grid = generate_crack_grid(initial_crack, element_surface, 'crack_edge')
    write_file(crack_surface_grid, 'crack_surface.vtu')
    write_file(crack_edge_grid, 'crack_edge.vtu')



