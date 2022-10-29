from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON, vtkCell, vtkPlane, vtkPolygon, vtkPolyhedron, vtkTetra, vtkVertex
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
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


def clip_a_vtk_cell(vtk_cell: vtkCell, origin_point=None, normal_vector=None):
    origin_point = np.array(origin_point).reshape((3, ))
    normal_vector = np.array(normal_vector).reshape((3, ))
    temp_id_list = get_polyhedron_list(vtk_cell)

    u_grid = vtkUnstructuredGrid()
    temp_point_list = vtkPoints()
    u_grid.SetPoints(temp_point_list)
    for each_point in range(vtk_cell.GetNumberOfPoints()):
        u_grid.GetPoints().InsertNextPoint(vtk_cell.GetPoints().GetPoint(each_point))
    u_grid.InsertNextCell(VTK_POLYHEDRON, temp_id_list)

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

    clip_polygon = None
    for each_plane_1 in range(result_cell_1.GetNumberOfFaces()):
        temp_polygon_1: vtkPolygon = result_cell_1.GetFace(each_plane_1)
        for each_plane_2 in range(result_cell_2.GetNumberOfFaces()):
            temp_polygon_2: vtkPolygon = result_cell_2.GetFace(each_plane_2)
            if polygon_equal(temp_polygon_1, temp_polygon_2):
                clip_polygon = temp_polygon_1
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
    return clip_polygon


if __name__ == '__main__':
    points = vtkPoints()
    points.InsertPoint(0, (0, 0, 0))
    points.InsertPoint(1, (1, 0, 0))
    points.InsertPoint(2, (0, 1, 0))
    points.InsertPoint(3, (0, 0, 1))

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

    cell0 = ugrid.GetCell(0)
    cell1 = vtkPolyhedron()
    cell1.DeepCopy(cell0)
    print(cell0.GetFaces())
    print(cell1.GetFaces())
    print(cell0.GetNumberOfFaces())
    print(cell1.GetNumberOfFaces())
    # cell1: vtkCell = ugrid.GetCell(0)
    # clip_a_vtk_cell(cell1, (0.5, 0, 0), (1, 0, 0))

