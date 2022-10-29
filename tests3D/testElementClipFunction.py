from NMM.base.ElementClipFunction import clip_a_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from object.tetra_polyhedron import generate_tetra_polyhedron
import numpy as np
import random
import pytest

test_tetra = generate_tetra_polyhedron()


def test_clip_tetrahedron():
    for i in range(1000):
        while True:
            x = random.random()
            y = random.random()
            z = random.random()
            if x + y + z < 1:
                break
        origin_point = np.array((x, y, z)).reshape((3, ))
        while True:
            x = random.random()
            y = random.random()
            z = random.random()
            if x + y + z > 0:
                break
        normal_vector = np.array((x, y, z)).reshape((3, ))

        result_polygon = clip_a_vtk_cell(test_tetra, origin_point, normal_vector)
        assert result_polygon is not None
