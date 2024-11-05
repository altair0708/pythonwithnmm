from NMM.base.ElementClipFunction import clip_a_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON, vtkPolygon, vtkTetra
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
import numpy as np
import random


def generate_tetra_polyhedron(point_1=(0, 0, 0), point_2=(1, 0, 0), point_3=(0, 1, 0), point_4=(0, 0, 1)):
    point_list = vtkPoints()
    point_list.InsertNextPoint(point_1)
    point_list.InsertNextPoint(point_2)
    point_list.InsertNextPoint(point_3)
    point_list.InsertNextPoint(point_4)

    tetrahedron_list = vtkIdList()
    tetrahedron_list.InsertNextId(4)

    tetrahedron_list.InsertNextId(3)
    tetrahedron_list.InsertNextId(3)
    tetrahedron_list.InsertNextId(0)
    tetrahedron_list.InsertNextId(1)

    tetrahedron_list.InsertNextId(3)
    tetrahedron_list.InsertNextId(3)
    tetrahedron_list.InsertNextId(1)
    tetrahedron_list.InsertNextId(2)

    tetrahedron_list.InsertNextId(3)
    tetrahedron_list.InsertNextId(3)
    tetrahedron_list.InsertNextId(2)
    tetrahedron_list.InsertNextId(0)

    tetrahedron_list.InsertNextId(3)
    tetrahedron_list.InsertNextId(2)
    tetrahedron_list.InsertNextId(1)
    tetrahedron_list.InsertNextId(0)

    u_grid = vtkUnstructuredGrid()
    u_grid.InsertNextCell(VTK_POLYHEDRON, tetrahedron_list)
    u_grid.SetPoints(point_list)

    tetrahedron_cell = u_grid.GetCell(0)

    return tetrahedron_cell, tetrahedron_list, point_list, u_grid


def generate_polygon(point_0=(0, 0, 0), point_1=(1, 0, 0), point_2=(0, 1, 0)):
    point_list = vtkPoints()
    point_list.InsertNextPoint(point_0)
    point_list.InsertNextPoint(point_1)
    point_list.InsertNextPoint(point_2)

    temp_polygon = vtkPolygon()
    temp_polygon.GetPointIds().SetNumberOfIds(3)
    temp_polygon.GetPointIds().SetId(0, 0)
    temp_polygon.GetPointIds().SetId(1, 1)
    temp_polygon.GetPointIds().SetId(2, 2)
    temp_polygon.GetPoints().DeepCopy(point_list)

    # u_grid = vtkUnstructuredGrid()
    # u_grid.InsertNextCell(temp_polygon.GetCellType(), temp_polygon.GetPointIds())
    # u_grid.SetPoints(point_list)
    #
    # polygon_cell = u_grid.GetCell(0)

    return temp_polygon, point_list

def generate_tetrahedron(point_1=(0, 0, 0), point_2=(1, 0, 0), point_3=(0, 1, 0), point_4=(0, 0, 1)):

    tetra_1 = vtkTetra()
    tetra_1.GetPointIds().SetId(0, 0)
    tetra_1.GetPointIds().SetId(1, 1)
    tetra_1.GetPointIds().SetId(2, 2)
    tetra_1.GetPointIds().SetId(3, 3)

    points = vtkPoints()
    points.InsertNextPoint(point_1)
    points.InsertNextPoint(point_2)
    points.InsertNextPoint(point_3)
    points.InsertNextPoint(point_4)

    u_grid = vtkUnstructuredGrid()
    u_grid.InsertNextCell(tetra_1.GetCellType(), tetra_1.GetPointIds())
    u_grid.SetPoints(points)

    new_tetra = u_grid.GetCell(0)

    return new_tetra, u_grid

if __name__ == '__main__':
    tetra, grid = generate_tetrahedron()
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetInputData(grid)
    writer.SetFileName('gmsh_tetrahedron.vtu')
    writer.Write()
