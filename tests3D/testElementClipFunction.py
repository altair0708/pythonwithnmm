from NMM.base.ElementClipFunction import clip_a_vtk_cell, polygon_equal
from NMM.base.CopyFunction import copy_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
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

def test_polygon_equal():
    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName('error_1.vtu')
    reader.Update()
    grid_1: vtkUnstructuredGrid = reader.GetOutput()

    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName('error_2.vtu')
    reader.Update()
    grid_2: vtkUnstructuredGrid = reader.GetOutput()
    result_cell_1 = grid_1.GetCell(0)
    result_cell_2 = grid_2.GetCell(0)

    for each_plane_1 in range(result_cell_1.GetNumberOfFaces()):
        temp_polygon_1: vtkPolygon = result_cell_1.GetFace(each_plane_1)
        for each_plane_2 in range(result_cell_2.GetNumberOfFaces()):
            temp_polygon_2: vtkPolygon = result_cell_2.GetFace(each_plane_2)
            if polygon_equal(temp_polygon_1, temp_polygon_2):
                clip_surface = copy_vtk_cell(temp_polygon_1, temp_polygon_1)
