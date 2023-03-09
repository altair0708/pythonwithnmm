import numpy as np
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.base.CopyFunction import copy_vtk_cell, copy_polyhedron
from NMM.base.PropertyGetSetFunction import get_property, set_property
from NMM.base.ModifyVtkCell import insert_a_cell, insert_a_cell_0
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray


def generate_crack_surface_file(mesh_path: str, geometry_path: str):

    # element file
    # surface file
    # crack surface file
    # edge file

    manifold_element_file = 'manifold_element.vtu'
    initial_crack_file = 'initial_crack.vtu'
    element_surface_file = 'element_surface.vtu'

    crack_surface_grid = vtkUnstructuredGrid()
    crack_surface_element_cell_data = vtkIntArray()
    crack_surface_element_cell_data.SetName('element_id')
    crack_surface_element_cell_data.SetNumberOfComponents(1)
    crack_surface_grid.GetCellData().AddArray(crack_surface_element_cell_data)

    edge_grid = vtkUnstructuredGrid()
    edge_surface_cell_data = vtkIntArray()
    edge_surface_cell_data.SetName('surface_id')
    edge_surface_cell_data.SetNumberOfComponents(1)
    edge_grid.GetCellData().AddArray(edge_surface_cell_data )

    element_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + manifold_element_file)
    element_number = element_grid.GetNumberOfCells()

    surface_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + element_surface_file)
    surface_edge_cell_data = vtkIntArray()
    surface_edge_cell_data.SetName('edge_id')
    surface_edge_cell_data.SetNumberOfComponents(1)
    surface_number = surface_grid.GetNumberOfCells()
    surface_edge_cell_data.SetNumberOfValues(surface_number)
    [surface_edge_cell_data.InsertValue(i, -1) for i in range(surface_number)]
    surface_grid.GetCellData().AddArray(surface_edge_cell_data)

    initial_crack_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(mesh_path + initial_crack_file)
    initial_crack_polygon: vtkPolygon = initial_crack_grid.GetCell(0)
    initial_crack_polygon: vtkPolygon = copy_vtk_cell(initial_crack_polygon, initial_crack_grid.GetPoints())

    # compute the normal vector and origin point of the plane of the initial crack polygon
    normal = [0, 0, 0]
    temp_polygon_points: vtkPoints = initial_crack_polygon.GetPoints()
    vtkPolygon.ComputeNormal(temp_polygon_points, normal)
    origin = temp_polygon_points.GetPoint(0)

    for each_element_id in range(element_number):
        temp_element_vtk_cell = element_grid.GetCell(each_element_id)
        # temp_element_vtk_cell = copy_vtk_cell(temp_element_vtk_cell, element_grid.GetPoints())
        temp_element_vtk_cell = copy_polyhedron(temp_element_vtk_cell, element_grid.GetPoints())
        if temp_element_vtk_cell.IntersectWithCell(initial_crack_polygon):
            try:
                temp_crack_surface_vtk_cell, _, _ = clip_a_vtk_cell(temp_element_vtk_cell, origin_point=origin, normal_vector=normal)
            except AssertionError:
                continue
            temp_crack_surface_id = crack_surface_grid.GetNumberOfCells()
            # cracked flag: 9 is initial crack
            set_property(element_grid, 'cracked', each_element_id, np.array((9,)))
            set_property(element_grid, 'crack_surface_id', each_element_id, np.array((temp_crack_surface_id,)))

            # insert_a_cell(crack_surface_grid, temp_crack_surface_vtk_cell)
            insert_a_cell_0(crack_surface_grid, temp_crack_surface_vtk_cell)
            set_property(crack_surface_grid, 'element_id', temp_crack_surface_id, np.array((each_element_id, )))
            # crackElementId.InsertNextValue(each_id)

            temp_element_surface_list = get_property(element_grid, 'surface_id', each_element_id)
            assert len(temp_element_surface_list) == 4
            for i, each_surface_id in enumerate(temp_element_surface_list):
                each_surface_id = int(each_surface_id)
                temp_surface_vtk_cell = surface_grid.GetCell(each_surface_id)
                temp_surface_vtk_cell = copy_vtk_cell(temp_surface_vtk_cell, surface_grid.GetPoints())
                try:
                    temp_edge_vtk_cell, _, _ = clip_a_vtk_cell(temp_surface_vtk_cell, origin_point=origin, normal_vector=normal)
                except AssertionError:
                    continue
                temp_edge_id = edge_grid.GetNumberOfCells()

                # cracked flag: 9 is initial crack
                set_property(surface_grid, 'cracked', each_surface_id, np.array((9,)))
                set_property(surface_grid, 'edge_id', each_surface_id, np.array((temp_edge_id,)))

                # insert_a_cell(edge_grid, temp_edge_vtk_cell)
                insert_a_cell_0(edge_grid, temp_edge_vtk_cell)
                set_property(edge_grid, 'surface_id', temp_edge_id, np.array((each_surface_id,)))

    def write_vtk_model(vtk_model, vtk_file_name, path):
        crackWriter = vtkXMLUnstructuredGridWriter()
        crackWriter.SetFileName(path + vtk_file_name)
        crackWriter.SetInputData(vtk_model)
        crackWriter.Write()

    write_vtk_model(element_grid, 'manifold_element.vtu', geometry_path)
    write_vtk_model(crack_surface_grid, 'crack_surface.vtu', geometry_path)
    write_vtk_model(surface_grid, 'element_surface.vtu', geometry_path)
    write_vtk_model(edge_grid, 'crack_edge.vtu', geometry_path)


def generate_crack_surface_file_0(mesh_path: str, geometry_path: str, initial_crack_file: str = 'initial_crack.vtu'):

    # element file
    # surface file
    # crack surface file
    # edge file

    manifold_element_file = 'manifold_element.vtu'
    element_surface_file = 'element_surface.vtu'

    crack_surface_grid = vtkUnstructuredGrid()
    crack_surface_element_cell_data = vtkIntArray()
    crack_surface_element_cell_data.SetName('element_id')
    crack_surface_element_cell_data.SetNumberOfComponents(1)
    crack_surface_grid.GetCellData().AddArray(crack_surface_element_cell_data)

    edge_grid = vtkUnstructuredGrid()
    edge_surface_cell_data = vtkIntArray()
    edge_surface_cell_data.SetName('surface_id')
    edge_surface_cell_data.SetNumberOfComponents(1)
    edge_grid.GetCellData().AddArray(edge_surface_cell_data )

    element_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + manifold_element_file)
    element_number = element_grid.GetNumberOfCells()

    surface_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + element_surface_file)
    surface_edge_cell_data = vtkIntArray()
    surface_edge_cell_data.SetName('edge_id')
    surface_edge_cell_data.SetNumberOfComponents(1)
    surface_number = surface_grid.GetNumberOfCells()
    surface_edge_cell_data.SetNumberOfValues(surface_number)
    [surface_edge_cell_data.InsertValue(i, -1) for i in range(surface_number)]
    surface_grid.GetCellData().AddArray(surface_edge_cell_data)

    initial_crack_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(mesh_path + initial_crack_file)
    for each_polygon_id in range(initial_crack_grid.GetNumberOfCells()):
        initial_crack_polygon: vtkPolygon = initial_crack_grid.GetCell(each_polygon_id)
        initial_crack_polygon: vtkPolygon = copy_vtk_cell(initial_crack_polygon, initial_crack_grid.GetPoints())

        # compute the normal vector and origin point of the plane of the initial crack polygon
        normal = [0, 0, 0]
        temp_polygon_points: vtkPoints = initial_crack_polygon.GetPoints()
        vtkPolygon.ComputeNormal(temp_polygon_points, normal)
        origin = temp_polygon_points.GetPoint(0)

        for each_element_id in range(element_number):
            temp_element_vtk_cell = element_grid.GetCell(each_element_id)
            # temp_element_vtk_cell = copy_vtk_cell(temp_element_vtk_cell, element_grid.GetPoints())
            temp_element_vtk_cell = copy_polyhedron(temp_element_vtk_cell, element_grid.GetPoints())
            if temp_element_vtk_cell.IntersectWithCell(initial_crack_polygon):
                try:
                    temp_crack_surface_vtk_cell, _, _ = clip_a_vtk_cell(temp_element_vtk_cell, origin_point=origin, normal_vector=normal)
                except AssertionError:
                    continue
                temp_crack_surface_id = crack_surface_grid.GetNumberOfCells()
                # cracked flag: 9 is initial crack
                set_property(element_grid, 'cracked', each_element_id, np.array((9,)))
                set_property(element_grid, 'crack_surface_id', each_element_id, np.array((temp_crack_surface_id,)))

                # insert_a_cell(crack_surface_grid, temp_crack_surface_vtk_cell)
                insert_a_cell_0(crack_surface_grid, temp_crack_surface_vtk_cell)
                set_property(crack_surface_grid, 'element_id', temp_crack_surface_id, np.array((each_element_id, )))
                # crackElementId.InsertNextValue(each_id)

                temp_element_surface_list = get_property(element_grid, 'surface_id', each_element_id)
                assert len(temp_element_surface_list) == 4
                for i, each_surface_id in enumerate(temp_element_surface_list):
                    each_surface_id = int(each_surface_id)
                    temp_surface_vtk_cell = surface_grid.GetCell(each_surface_id)
                    temp_surface_vtk_cell = copy_vtk_cell(temp_surface_vtk_cell, surface_grid.GetPoints())
                    try:
                        temp_edge_vtk_cell, _, _ = clip_a_vtk_cell(temp_surface_vtk_cell, origin_point=origin, normal_vector=normal)
                    except AssertionError:
                        continue
                    temp_edge_id = edge_grid.GetNumberOfCells()

                    # cracked flag: 9 is initial crack
                    set_property(surface_grid, 'cracked', each_surface_id, np.array((9,)))
                    set_property(surface_grid, 'edge_id', each_surface_id, np.array((temp_edge_id,)))

                    # insert_a_cell(edge_grid, temp_edge_vtk_cell)
                    insert_a_cell_0(edge_grid, temp_edge_vtk_cell)
                    set_property(edge_grid, 'surface_id', temp_edge_id, np.array((each_surface_id,)))

    def write_vtk_model(vtk_model, vtk_file_name, path):
        crackWriter = vtkXMLUnstructuredGridWriter()
        crackWriter.SetFileName(path + vtk_file_name)
        crackWriter.SetInputData(vtk_model)
        crackWriter.Write()

    write_vtk_model(element_grid, 'manifold_element.vtu', geometry_path)
    write_vtk_model(crack_surface_grid, 'crack_surface.vtu', geometry_path)
    write_vtk_model(surface_grid, 'element_surface.vtu', geometry_path)
    write_vtk_model(edge_grid, 'crack_edge.vtu', geometry_path)
