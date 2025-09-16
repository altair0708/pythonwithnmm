from NMM.base.VTKBase import get_a_vtk_cell_grid, is_intersect, debug_write_file, clip_a_element, clip_a_surface, check_point_in_cell
from NMM.base.VTKBase.triangulate_crack_advance import triangle_and_iterate_grid
from NMM.base.VTKBase.intersection_line_with_triangle import intersect_line_with_triangle
from NMM.base.VTKBase.iterate_polyhedron_edge import iterate_polyhedron_edges


def test_crack_intersection():

    crack_iteration = triangle_and_iterate_grid(each_crack_polygon_grid)
    edge_iteration = iterate_polyhedron_edges(each_manifold_element)

    crack_point_count = 0
    crack_point_list = []
    for each_edge in edge_iteration:
        for each_crack_triangle in crack_iteration:
            result = intersect_line_with_triangle(each_edge, each_crack_triangle)
            if result is not None:
                crack_point_count = crack_point_count + 1
                crack_point_list.append(result)
