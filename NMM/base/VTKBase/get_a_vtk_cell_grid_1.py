from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPolygon, VTK_POLYHEDRON, vtkCellArray
from vtkmodules.vtkFiltersCore import vtkRemoveUnusedPoints, vtkConvertToPolyhedra
from vtkmodules.vtkFiltersExtraction import vtkExtractUnstructuredGrid
from vtkmodules.vtkFiltersGeneral import vtkCleanUnstructuredGrid
from NMM.base.VTKBase import get_cell_attribute
from typing import List


def get_a_vtk_cell_grid(vtk_model: vtkUnstructuredGrid, id_value: int, turn_polyhedron=False) -> vtkUnstructuredGrid:

    extractor = vtkExtractUnstructuredGrid()
    extractor.SetInputData(vtk_model)
    extractor.CellClippingOn()
    extractor.SetCellMaximum(id_value)
    extractor.SetCellMinimum(id_value)
    output_port = extractor

    if turn_polyhedron:
        converter = vtkConvertToPolyhedra()
        converter.SetInputConnection(extractor.GetOutputPort())
        output_port = converter

    # clean unused points
    cleaner = vtkCleanUnstructuredGrid()
    cleaner.RemovePointsWithoutCellsOn()
    cleaner.SetInputConnection(output_port.GetOutputPort())
    cleaner.Update()
    result = cleaner.GetOutput()
    return result


