#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter, vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkHexahedron,
    vtkPlane,
    vtkUnstructuredGrid
)
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    # Setup the coordinates of eight points
    # (the two faces must be in counter clockwise order as viewed from the
    # outside)
    pointCoords = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0],
        [0.0, 0.0, 2.0],
        [1.0, 0.0, 2.0],
        [1.0, 1.0, 2.0],
        [0.0, 1.0, 2.0]
    ]

    # Create the points and a hexahedron from the points.
    points = vtkPoints()
    hexa1 = vtkHexahedron()
    hexa2 = vtkHexahedron()
    for i, pointCoord in enumerate(pointCoords):
        points.InsertNextPoint(pointCoord)
    for i in range(8):
        hexa1.GetPointIds().SetId(i, i)
        hexa2.GetPointIds().SetId(i, i + 4)

    # Add the hexahedron to a cell array.
    hexs = vtkCellArray()
    hexs.InsertNextCell(hexa1)
    hexs.InsertNextCell(hexa2)

    # Add the points and hexahedron to an unstructured grid.
    uGrid = vtkUnstructuredGrid()
    uGrid.SetPoints(points)
    uGrid.InsertNextCell(hexa1.GetCellType(), hexa1.GetPointIds())
    uGrid.InsertNextCell(hexa2.GetCellType(), hexa2.GetPointIds())
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName('surface.vtu')
    writer.SetInputData(uGrid)
    writer.Write()

    # Extract the outer (polygonal) surface.
    surface = vtkDataSetSurfaceFilter()
    surface.SetInputData(uGrid)
    surface.Update()
    result = surface.GetOutput()
    writer = vtkXMLPolyDataWriter()
    writer.SetFileName('surface.vtp')
    writer.SetInputData(result)
    writer.Write()

if __name__ == '__main__':
    main()