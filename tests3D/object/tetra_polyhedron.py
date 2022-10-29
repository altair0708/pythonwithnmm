from NMM.base.ElementClipFunction import clip_a_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
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

    return tetrahedron_cell
