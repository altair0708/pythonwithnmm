from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON, vtkCell, vtkPlane, vtkPolygon, vtkPolyhedron, vtkTetra, vtkVertex
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.base.CopyFunction import copy_vtk_cell
import numpy as np


def get_polyhedron_list(vtk_cell: vtkCell):
    id_list = vtkIdList()
    id_list.InsertNextId(vtk_cell.GetNumberOfFaces())
    for each_face in range(vtk_cell.GetNumberOfFaces()):
        temp_face: vtkPolygon = vtk_cell.GetFace(each_face)
        id_list.InsertNextId(temp_face.GetNumberOfPoints())
        face_id_list: vtkIdList = temp_face.GetPointIds()
        for each_point in range(temp_face.GetNumberOfPoints()):
            temp_id = face_id_list.GetId(each_point)
            id_list.InsertNextId(temp_id)
    return id_list


def generate_vtk_plane(vtk_points: vtkPoints):
    points_1 = vtk_points
    vector_1 = np.array(points_1.GetPoint(0)) - np.array(points_1.GetPoint(1))
    vector_2 = np.array(points_1.GetPoint(0)) - np.array(points_1.GetPoint(2))

    normal_vector = tuple(np.cross(vector_1, vector_2))
    origin_point = points_1.GetPoint(0)

    vtk_plane = vtkPlane()
    vtk_plane.SetNormal(normal_vector)
    vtk_plane.SetOrigin(origin_point)

    return vtk_plane


def clip_a_vtk_cell(vtk_cell: vtkCell, origin_point=None, normal_vector=None):
    origin_point = np.array(origin_point).reshape((3, ))
    normal_vector = np.array(normal_vector).reshape((3, ))

    u_grid = vtkUnstructuredGrid()
    temp_point_list = vtkPoints()
    u_grid.SetPoints(temp_point_list)
    for each_point in range(vtk_cell.GetNumberOfPoints()):
        u_grid.GetPoints().InsertNextPoint(vtk_cell.GetPoints().GetPoint(each_point))

    if vtk_cell.GetCellType() == VTK_POLYHEDRON:
        temp_id_list = get_polyhedron_list(vtk_cell)
        u_grid.InsertNextCell(VTK_POLYHEDRON, temp_id_list)
    else:
        u_grid.InsertNextCell(vtk_cell.GetCellType(), vtk_cell.GetPointIds())

    clip_plane_1 = vtkPlane()
    clip_plane_1.SetOrigin(origin_point)
    clip_plane_1.SetNormal(normal_vector)

    counter_normal = tuple(-i for i in normal_vector)
    clip_plane_2 = vtkPlane()
    clip_plane_2.SetOrigin(origin_point)
    clip_plane_2.SetNormal(counter_normal)

    def clip(grid: vtkUnstructuredGrid, plane: vtkPlane):
        clipper = vtkClipDataSet()
        clipper.SetClipFunction(plane)
        clipper.SetInputData(grid)
        clipper.Update()
        result: vtkUnstructuredGrid = clipper.GetOutput()
        return result

    grid_1 = clip(u_grid, clip_plane_1)
    grid_2 = clip(u_grid, clip_plane_2)

    result_cell_1: vtkCell = grid_1.GetCell(0)
    result_cell_2: vtkCell = grid_2.GetCell(0)

    clip_polygon = None
    for each_plane_1 in range(result_cell_1.GetNumberOfFaces()):
        temp_polygon_1: vtkPolygon = result_cell_1.GetFace(each_plane_1)
        for each_plane_2 in range(result_cell_2.GetNumberOfFaces()):
            temp_polygon_2: vtkPolygon = result_cell_2.GetFace(each_plane_2)
            if polygon_equal(temp_polygon_1, temp_polygon_2):
                clip_polygon = copy_vtk_cell(temp_polygon_1, grid_1.GetPoints())
    if clip_polygon is None:
        tetra_1 = vtkTetra()
        tetra_1.GetPointIds().SetId(0, 0)
        tetra_1.GetPointIds().SetId(1, 1)
        tetra_1.GetPointIds().SetId(2, 2)
        tetra_1.GetPointIds().SetId(3, 3)

        vertex_1 = vtkVertex()
        vertex_1.GetPointIds().SetId(0, 4)

        error_points = vtkPoints()
        error_points.DeepCopy(u_grid.GetPoints())
        error_points.InsertNextPoint(origin_point)

        error_grid = vtkUnstructuredGrid()
        error_grid.InsertNextCell(tetra_1.GetCellType(), tetra_1.GetPointIds())
        error_grid.InsertNextCell(vertex_1.GetCellType(), vertex_1.GetPointIds())
        error_grid.SetPoints(error_points)

        writer = vtkXMLUnstructuredGridWriter()
        writer.SetInputData(error_grid)
        writer.SetFileName('error_1.vtu')
        writer.Write()
    return clip_polygon, grid_1, grid_2


def polygon_equal(polygon_1: vtkPolygon, polygon_2: vtkPolygon):
    number_1 = polygon_1.GetNumberOfPoints()
    number_2 = polygon_2.GetNumberOfPoints()
    if number_1 != number_2:
        return False

    point_list_1: vtkPoints = polygon_1.GetPoints()
    point_list_2: vtkPoints = polygon_2.GetPoints()
    point_set_1 = set()
    point_set_2 = set()
    for each_point in range(number_1):
        point_set_1.add(point_list_1.GetPoint(each_point))
        point_set_2.add(point_list_2.GetPoint(each_point))

    if point_set_1 == point_set_2:
        return True
    else:
        return False


def generate_crack_edge_surface(adjacent_element: list, crack_surface: vtkPolygon):
    edge_list = []
    for each_edge in range(crack_surface.GetNumberOfEdges()):
        temp_points = vtkPoints()
        temp_edge = crack_surface.GetEdge(each_edge)
        temp_points.DeepCopy(temp_edge.GetPoints())
        edge_list.append(temp_points)

    for each_dict in adjacent_element:
        for edge_points in edge_list:
            if check_coplanar(each_dict['face_points'], edge_points):
                temp_edge_points = vtkPoints()
                temp_edge_points.DeepCopy(edge_points)
                each_dict['edge_points'] = temp_edge_points


def check_coplanar(surface_points: vtkPoints, edge_points: vtkPoints):

    assert edge_points.GetNumberOfPoints() == 2

    points_1 = surface_points
    vector_1 = np.array(points_1.GetPoint(0)) - np.array(points_1.GetPoint(1))
    vector_2 = np.array(points_1.GetPoint(0)) - np.array(points_1.GetPoint(2))

    normal_vector = tuple(np.cross(vector_1, vector_2))
    origin_point = points_1.GetPoint(0)

    vtk_plane = vtkPlane()
    vtk_plane.SetNormal(normal_vector)
    vtk_plane.SetOrigin(origin_point)

    coplanar_list = []
    for each_point in range(edge_points.GetNumberOfPoints()):
        temp_point = edge_points.GetPoint(each_point)
        if -10**(-5) < vtk_plane.EvaluateFunction(temp_point) < 10**(-5):
            coplanar_list.append(temp_point)

    if len(coplanar_list) == 2:
        return True
    else:
        return False


def calculate_mass_center(vtk_cell: vtkCell):
    temp_cell: vtkCell = vtk_cell
    point_number = temp_cell.GetNumberOfPoints()
    point_list: vtkPoints = temp_cell.GetPoints()

    # calculate mass center
    x = 0
    y = 0
    z = 0
    for each_point in range(point_number):
        x = x + point_list.GetPoint(each_point)[0]
        y = y + point_list.GetPoint(each_point)[1]
        z = z + point_list.GetPoint(each_point)[2]
    center = np.array((x / point_number, y / point_number, z / point_number)).reshape((3, ))
    return center

if __name__ == '__main__':
    points = vtkPoints()
    points.InsertPoint(0, (2.0, 0.5099039077758789, -0.6648310422897339))
    points.InsertPoint(1, (2.0, -0.23611851036548615, 1.1471405029296875))
    points.InsertPoint(2, (2.0, -1.432482361793518, -0.4047808349132538))
    points.InsertPoint(3, (0.0, -0.23611851036548615, 1.1471405029296875))

    point_id = vtkIdList()
    point_id.InsertNextId(4)

    point_id.InsertNextId(3)
    point_id.InsertNextId(0)
    point_id.InsertNextId(1)
    point_id.InsertNextId(2)

    point_id.InsertNextId(3)
    point_id.InsertNextId(0)
    point_id.InsertNextId(2)
    point_id.InsertNextId(3)

    point_id.InsertNextId(3)
    point_id.InsertNextId(0)
    point_id.InsertNextId(3)
    point_id.InsertNextId(1)

    point_id.InsertNextId(3)
    point_id.InsertNextId(3)
    point_id.InsertNextId(2)
    point_id.InsertNextId(1)

    ugrid = vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(VTK_POLYHEDRON, point_id)

    cell0: vtkCell = ugrid.GetCell(0)
    center = [1.5, -0.34870387, 0.30616728]
    direct = [0.99959329, -0.02529452, -0.01316967]
    surface = clip_a_vtk_cell(cell0, center, direct)

    insert_a_cell(ugrid, surface)
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName('error.vtu')
    writer.SetInputData(ugrid)
    writer.Write()

    face_dictionary = []
    for each_face in range(cell0.GetNumberOfFaces()):
        adjacent_face_points = vtkPoints()
        temp_face = cell0.GetFace(each_face)
        adjacent_face_points.DeepCopy(temp_face.GetPoints())
        print(adjacent_face_points.GetNumberOfPoints())

        face_dictionary.append({'face_id': each_face, 'adjacent_cell_id': 0, 'face_points': adjacent_face_points})

    generate_crack_edge_surface(face_dictionary, surface)
    [print(i) for i in face_dictionary]


