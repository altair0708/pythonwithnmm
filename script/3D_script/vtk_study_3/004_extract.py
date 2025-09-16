from NMM.base.VTKBase.extract_cells_in_box import extract_cells_in_box
from NMM.base.VTKBase import load_a_grid, write_file
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.intersection_box import intersection_grid, intersection_box
from NMM.base.VTKBase.iterate_polyhedron_edge import iterate_polyhedron_edges
from NMM.base.VTKBase.intersection_line_with_polydata import intersection_line_with_polydata_cache,  intersection_line_with_polydata
from NMM.base.VTKBase.is_empty_cell import is_empty_cell
import timeit

crack = VtkGrid('crack', 'crack_propagation.vtu')
vtk_model = VtkGrid('vtk_model', 'manifold_element.vtu')

id_list = set()
for each_id, each_grid in enumerate(vtk_model):
    if is_empty_cell(each_grid):
        continue
    if intersection_box(crack.value, each_grid):
        id_list.add(each_id)


crack_point_dict = {}
for each_id in id_list:
    each_manifold_element = vtk_model[each_id]
    edge_iteration = iterate_polyhedron_edges(each_manifold_element)

    crack_point_list = []
    for each_edge in edge_iteration:
        result, point = intersection_line_with_polydata_cache(crack.value, each_edge)
        if result:
            crack_point_list.append(point)
    crack_point_dict.setdefault(each_id, []).extend(crack_point_list)
print(crack_point_dict[885])

