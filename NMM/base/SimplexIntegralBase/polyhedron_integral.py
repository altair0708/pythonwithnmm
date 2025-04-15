import numpy as np
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON


def once_integration(vtk_model: vtkUnstructuredGrid):
    assert vtk_model.GetNumberOfCells() == 1
    assert vtk_model.GetCell(0).GetCellType() == VTK_POLYHEDRON

    vtk_cell = vtk_model.GetCell(0)
    points = vtk_cell.GetPoints()

    S = 0
    xS = 0
    yS = 0
    zS = 0
    p0 = (0, 0, 0)
    for each_surface_id in range(vtk_cell.GetNumberOfFaces()):
        surface = vtk_cell.GetFace(each_surface_id)
        p1_id = surface.GetPointId(0)
        p1 = points.GetPoint(p1_id)
        for each_edge_id in range(surface.GetNumberOfEdges()):
            edge = surface.GetEdge(each_edge_id)

            p2_id = edge.GetPointId(0)
            p2 = points.GetPoint(p2_id)

            p3_id = edge.GetPointId(1)
            p3 = points.GetPoint(p3_id)

            temp_matrix = np.array([[p1[0], p1[1], p1[2]],
                                    [p2[0], p2[1], p2[2]],
                                    [p3[0], p3[1], p3[2]]])

            temp_s = (1 / 6) * (np.linalg.det(temp_matrix))
            temp_xs = (1 / 24) * (np.linalg.det(temp_matrix)) * (p1[0] + p2[0] + p3[0])
            temp_ys = (1 / 24) * (np.linalg.det(temp_matrix)) * (p1[1] + p2[1] + p3[1])
            temp_zs = (1 / 24) * (np.linalg.det(temp_matrix)) * (p1[2] + p2[2] + p3[2])

            S = S + temp_s
            xS = xS + temp_xs
            yS = yS + temp_ys
            zS = zS + temp_zs

    return S, xS, yS, zS


def twice_integration(vtk_model: vtkUnstructuredGrid):
    assert vtk_model.GetNumberOfCells() == 1
    assert vtk_model.GetCell(0).GetCellType() == VTK_POLYHEDRON

    vtk_cell = vtk_model.GetCell(0)
    points = vtk_cell.GetPoints()

    xxS = 0
    yyS = 0
    zzS = 0
    xyS = 0
    xzS = 0
    yzS = 0
    p0 = (0, 0, 0)
    for each_surface_id in range(vtk_cell.GetNumberOfFaces()):
        surface = vtk_cell.GetFace(each_surface_id)
        p1_id = surface.GetPointId(0)
        p1 = points.GetPoint(p1_id)
        for each_edge_id in range(surface.GetNumberOfEdges()):
            edge = surface.GetEdge(each_edge_id)

            p2_id = edge.GetPointId(0)
            p2 = points.GetPoint(p2_id)

            p3_id = edge.GetPointId(1)
            p3 = points.GetPoint(p3_id)

            temp_matrix = np.array([[p1[0], p1[1], p1[2]],
                                    [p2[0], p2[1], p2[2]],
                                    [p3[0], p3[1], p3[2]]])

            temp_xxs = (np.linalg.det(temp_matrix)) * (2 * p1[0] * p1[0] + 1 * p1[0] * p2[0] + 1 * p1[0] * p3[0] +
                                                       1 * p2[0] * p1[0] + 2 * p2[0] * p2[0] + 1 * p2[0] * p3[0] +
                                                       1 * p3[0] * p1[0] + 1 * p3[0] * p2[0] + 2 * p3[0] * p3[0])

            temp_yys = (np.linalg.det(temp_matrix)) * (2 * p1[1] * p1[1] + 1 * p1[1] * p2[1] + 1 * p1[1] * p3[1] +
                                                       1 * p2[1] * p1[1] + 2 * p2[1] * p2[1] + 1 * p2[1] * p3[1] +
                                                       1 * p3[1] * p1[1] + 1 * p3[1] * p2[1] + 2 * p3[1] * p3[1])

            temp_zzs = (np.linalg.det(temp_matrix)) * (2 * p1[2] * p1[2] + 1 * p1[2] * p2[2] + 1 * p1[2] * p3[2] +
                                                       1 * p2[2] * p1[2] + 2 * p2[2] * p2[2] + 1 * p2[2] * p3[2] +
                                                       1 * p3[2] * p1[2] + 1 * p3[2] * p2[2] + 2 * p3[2] * p3[2])

            temp_xys = (np.linalg.det(temp_matrix)) * (2 * p1[0] * p1[1] + 1 * p1[0] * p2[1] + 1 * p1[0] * p3[1] +
                                                       1 * p2[0] * p1[1] + 2 * p2[0] * p2[1] + 1 * p2[0] * p3[1] +
                                                       1 * p3[0] * p1[1] + 1 * p3[0] * p2[1] + 2 * p3[0] * p3[1])

            temp_xzs = (np.linalg.det(temp_matrix)) * (2 * p1[0] * p1[2] + 1 * p1[0] * p2[2] + 1 * p1[0] * p3[2] +
                                                       1 * p2[0] * p1[2] + 2 * p2[0] * p2[2] + 1 * p2[0] * p3[2] +
                                                       1 * p3[0] * p1[2] + 1 * p3[0] * p2[2] + 2 * p3[0] * p3[2])

            temp_yzs = (np.linalg.det(temp_matrix)) * (2 * p1[1] * p1[2] + 1 * p1[1] * p2[2] + 1 * p1[1] * p3[2] +
                                                       1 * p2[1] * p1[2] + 2 * p2[1] * p2[2] + 1 * p2[1] * p3[2] +
                                                       1 * p3[1] * p1[2] + 1 * p3[1] * p2[2] + 2 * p3[1] * p3[2])

            xxS = xxS + (1 / 120) * temp_xxs
            yyS = yyS + (1 / 120) * temp_yys
            zzS = zzS + (1 / 120) * temp_zzs
            xyS = xyS + (1 / 120) * temp_xys
            xzS = xzS + (1 / 120) * temp_xzs
            yzS = yzS + (1 / 120) * temp_yzs

    return xxS, yyS, zzS, xyS, xzS, yzS
