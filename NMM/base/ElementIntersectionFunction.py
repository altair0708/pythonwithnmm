from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, mutable
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra, vtkCell, vtkPolygon, vtkLine, vtkPlane
from tests3D.object.tetra_polyhedron import generate_tetra_polyhedron, generate_polygon
import numpy as np


def get_edge_list(vtk_cell: vtkCell):
    edge_number = vtk_cell.GetNumberOfEdges()
    edge_list = []
    for edge_id in range(edge_number):
        temp_edge: vtkLine = vtk_cell.GetEdge(edge_id)
        point_0 = temp_edge.GetPoints().GetPoint(0)
        point_1 = temp_edge.GetPoints().GetPoint(1)
        edge_list.append((point_0, point_1))
    return edge_list


def get_polygon_plane(vtk_polygon: vtkPolygon):
    point_number = vtk_polygon.GetNumberOfPoints()
    point_list = []
    for point_id in range(point_number):
        temp_points = vtk_polygon.GetPoints()
        temp_point = temp_points.GetPoint(point_id)
        point_list.append(temp_point)

    origin_point = point_list[0]

    vector_0 = np.array(point_list[1]) - np.array((point_list[0]))
    vector_1 = np.array(point_list[2]) - np.array((point_list[0]))

    normal_vector = np.cross(vector_0, vector_1)
    normal_vector = tuple(normal_vector)

    return point_list, origin_point, normal_vector


def check_intersect(vtk_polygon: vtkPolygon, vtk_cell: vtkCell):
    edges = get_edge_list(vtk_cell)
    intersect_list = []
    for each_edge in edges:
        # Input
        point_0 = each_edge[0]
        point_1 = each_edge[1]
        tolerance = 0

        # Outputs
        t = mutable(0)  # Parametric coordinate of intersection (0 (corresponding to p1) to 1 (corresponding to p2))
        x = [0.0, 0.0, 0.0]
        pcoords = [0.0, 0.0, 0.0]
        subId = mutable(0)

        is_intersect = vtk_polygon.IntersectWithLine(point_0, point_1, tolerance, t, x, pcoords, subId)
        intersect_list.append(is_intersect)
    return intersect_list


if __name__ == '__main__':
    temp_tetra, _, _ = generate_tetra_polyhedron()
    temp_polygon_0, _ = generate_polygon(point_0=(0, 0, 0.5), point_1=(1, 0, 0.5), point_2=(0, 1, 0.5))
    print(get_edge_list(temp_tetra))
    intersect_list = check_intersect(temp_polygon_0, temp_tetra)
    print(sum(intersect_list))

