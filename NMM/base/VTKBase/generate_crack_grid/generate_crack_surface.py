from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints
from NMM.base.VTKBase.get_a_vtk_cell_grid import get_a_vtk_cell_grid
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell import insert_a_vtk_cell
from NMM.base.VTKBase.generate_crack_grid.is_intersect import is_intersect
from NMM.base.VTKBase.generate_crack_grid.clip_a_element.clip_a_element import clip_a_element
from NMM.base.VTKBase.new_a_grid import new_a_grid
from NMM.base.CacheBase.AttributeCache import attribute_cache
from NMM.base.CacheBase.GeometryCache import geometry_cache


def generate_crack_surface(crack_grid: vtkUnstructuredGrid, element_grid: vtkUnstructuredGrid):
    # compute the normal vector and origin point of the plane of the initial crack polygon
    assert crack_grid.GetNumberOfCells() == 1
    crack_polygon_grid: vtkUnstructuredGrid = get_a_vtk_cell_grid(crack_grid, 0)

    # normal vector, origin point
    normal = [0, 0, 0]
    temp_polygon_points: vtkPoints = crack_polygon_grid.GetPoints()
    vtkPolygon.ComputeNormal(temp_polygon_points, normal)
    origin = temp_polygon_points.GetPoint(0)

    crack_element_grid: vtkUnstructuredGrid = new_a_grid()
    for each_element_id in range(element_grid.GetNumberOfCells()):
        # each_element_grid: vtkUnstructuredGrid = get_a_vtk_cell_grid(element_grid, each_element_id, turn_polyhedron=True)
        each_element_grid: vtkUnstructuredGrid = get_a_vtk_cell_grid(element_grid, each_element_id)
        if is_intersect(crack_polygon_grid, each_element_grid):
            try:
                crack_surface_grid, new_element_0, new_element_1 = clip_a_element(each_element_grid, origin, normal)
            except AssertionError:
                continue

            attribute_cache.add_item('manifold_element', 'cracked', each_element_id, 9)
            geometry_cache.add_item('crack_surface', crack_surface_grid)
            geometry_cache.add_item('new_element', new_element_0)
            geometry_cache.add_item('new_element', new_element_1)
            insert_a_vtk_cell(crack_surface_grid, crack_element_grid)

    return crack_element_grid
