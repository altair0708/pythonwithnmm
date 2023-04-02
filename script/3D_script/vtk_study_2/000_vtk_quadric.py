#!/usr/bin/env python

from vtkmodules.vtkCommonDataModel import vtkQuadric, vtkUnstructuredGrid, vtkTetra, vtkPlane, vtkHexahedron
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader

# create an ellipsoid using a implicit quadric
quadric = vtkQuadric()
quadric.SetCoefficients(1, 1, 1, 0, 0, 0, -6, 0, 0, 0)

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName('re000_0.vtu')

clipper = vtkClipDataSet()
clipper.SetInputConnection(reader.GetOutputPort())
clipper.SetClipFunction(quadric)
clipper.Update()
result = clipper.GetOutput()

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('re000_1.vtu')
writer.SetInputData(result)
writer.Write()
