import numpy as np
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.base.CopyFunction import copy_vtk_cell, copy_polyhedron
from NMM.base.PropertyGetSetFunction import get_property, set_property
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray


def generate_crack_surface_file(initial_crack_file: str, manifold_element_file: str, output_path: str):
    crack_surface_grid = vtkUnstructuredGrid()
    crackElementId = vtkIntArray()
    crackElementId.SetName('element_id')
    crackElementId.SetNumberOfComponents(1)
    crack_surface_grid.GetCellData().AddArray(crackElementId)

    initial_crack_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(initial_crack_file)
    initial_crack_polygon: vtkPolygon = initial_crack_grid.GetCell(0)
    initial_crack_polygon: vtkPolygon = copy_vtk_cell(initial_crack_polygon, initial_crack_grid.GetPoints())

    # compute the normal vector and origin point of the plane of the initial crack polygon
    normal = [0, 0, 0]
    temp_polygon_points: vtkPoints = initial_crack_polygon.GetPoints()
    vtkPolygon.ComputeNormal(temp_polygon_points, normal)
    origin = temp_polygon_points.GetPoint(0)

    manifold_element_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(manifold_element_file)
    element_number = manifold_element_grid.GetNumberOfCells()

    for each_id in range(element_number):
        temp_vtk_cell = manifold_element_grid.GetCell(each_id)
        temp_vtk_cell = copy_vtk_cell(temp_vtk_cell, manifold_element_grid.GetPoints())
        # temp_vtk_cell = copy_polyhedron(temp_vtk_cell, manifold_element_grid.GetPoints())
        if temp_vtk_cell.IntersectWithCell(initial_crack_polygon):
            try:
                temp_crack_surface, _, _ = clip_a_vtk_cell(temp_vtk_cell, origin_point=origin, normal_vector=normal)
            except AssertionError:
                continue

            crack_surface_id = crack_surface_grid.GetNumberOfCells()
            set_property(manifold_element_grid, 'cracked', each_id, np.array((3,)))
            set_property(manifold_element_grid, 'crack_surface_id', each_id, np.array((crack_surface_id,)))

            insert_a_cell(crack_surface_grid, temp_crack_surface)
            crackElementId.InsertNextValue(each_id)

    def write_vtk_model(vtk_model, vtk_file_name, path):
        crackWriter = vtkXMLUnstructuredGridWriter()
        crackWriter.SetFileName(path + vtk_file_name)
        crackWriter.SetInputData(vtk_model)
        crackWriter.Write()

    write_vtk_model(manifold_element_grid, 'manifold_element.vtu', output_path)
    write_vtk_model(crack_surface_grid, 'crack_surface.vtu', output_path)
