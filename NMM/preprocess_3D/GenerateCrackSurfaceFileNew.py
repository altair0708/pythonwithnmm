import sys
import numpy as np
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.base.CopyFunction import copy_vtk_cell, copy_polyhedron
from NMM.base.WriteErrorVTU import write_error_vtu
from NMM.base.PropertyGetSetFunction import get_property, set_property
from NMM.base.ModifyVtkCell import insert_a_cell, insert_a_cell_0
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from NMM.base.CalculateArea import calculate_area
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray


def new_id_generator():
    id_value = 0
    while True:
        yield id_value
        id_value += 1


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

    # crack surface file generated
    crack_surface_grid = vtkUnstructuredGrid()
    crack_surface_element_cell_data = vtkIntArray()
    crack_surface_element_cell_data.SetName('element_id')
    crack_surface_element_cell_data.SetNumberOfComponents(1)
    crack_surface_grid.GetCellData().AddArray(crack_surface_element_cell_data)

    # crack edge file generated
    edge_grid = vtkUnstructuredGrid()
    edge_surface_cell_data = vtkIntArray()
    edge_surface_cell_data.SetName('surface_id')
    edge_surface_cell_data.SetNumberOfComponents(1)
    edge_grid.GetCellData().AddArray(edge_surface_cell_data )

    # open existed element file
    element_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + manifold_element_file)
    element_number = element_grid.GetNumberOfCells()

    # open existed element surface file
    surface_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + element_surface_file)
    surface_number = surface_grid.GetNumberOfCells()
    # add crack edge id
    surface_edge_cell_data = vtkIntArray()
    surface_edge_cell_data.SetName('edge_id')
    surface_edge_cell_data.SetNumberOfComponents(1)
    surface_edge_cell_data.SetNumberOfValues(surface_number)
    [surface_edge_cell_data.InsertValue(i, -1) for i in range(surface_number)]
    surface_grid.GetCellData().AddArray(surface_edge_cell_data)

    # open initial crack file, an entity plane, not scattered polygon
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
                    temp_crack_surface_vtk_cell, new_element_cell_grid_0, new_element_cell_grid_1 = clip_a_vtk_cell(temp_element_vtk_cell, origin_point=origin, normal_vector=normal)
                except AssertionError:
                    continue

                # build relationship of crack surface and element
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


def generate_crack_surface_file_1(mesh_path: str, geometry_path: str, initial_crack_file: str = 'initial_crack.vtu'):

    # element file
    # surface file
    # crack surface file
    # edge file

    manifold_element_file = 'manifold_element.vtu'
    element_surface_file = 'element_surface.vtu'

    # region: Initial element, surface, crack_surface, edge gird.
    # element
    element_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + manifold_element_file)
    element_number = element_grid.GetNumberOfCells()
    element_cell_data = vtkIntArray()
    element_cell_data.SetName('sub_element_id')
    element_cell_data.SetNumberOfComponents(2)
    element_cell_data.SetNumberOfValues(element_number)
    [element_cell_data.InsertTuple(i, (-1, -1)) for i in range(element_number)]
    element_grid.GetCellData().AddArray(element_cell_data)

    crackSurfaceNumber = vtkIntArray()
    crackSurfaceNumber.SetName('crack_surface_id')
    crackSurfaceNumber.SetNumberOfComponents(2)
    crackSurfaceNumber.SetNumberOfValues(element_number)
    [crackSurfaceNumber.InsertTuple(i, (-1, -1)) for i in range(element_number)]

    element_grid.GetCellData().AddArray(crackSurfaceNumber)

    # surface
    surface_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + element_surface_file)
    surface_number = surface_grid.GetNumberOfCells()

    surface_edge_cell_data = vtkIntArray()
    surface_edge_cell_data.SetName('edge_id')
    surface_edge_cell_data.SetNumberOfComponents(1)
    surface_edge_cell_data.SetNumberOfValues(surface_number)
    [surface_edge_cell_data.InsertValue(i, -1) for i in range(surface_number)]
    surface_grid.GetCellData().AddArray(surface_edge_cell_data)

    # crack surface
    crack_surface_grid = vtkUnstructuredGrid()

    crack_surface_element_cell_data = vtkIntArray()
    crack_surface_element_cell_data.SetName('element_id')
    crack_surface_element_cell_data.SetNumberOfComponents(1)

    temp_edge_id = vtkIntArray()
    temp_edge_id.SetNumberOfComponents(4)
    temp_edge_id.SetName('edge_id')

    crack_surface_grid.GetCellData().AddArray(crack_surface_element_cell_data)
    crack_surface_grid.GetCellData().AddArray(temp_edge_id)

    # crack edge
    edge_grid = vtkUnstructuredGrid()

    edge_surface_cell_data = vtkIntArray()
    edge_surface_cell_data.SetName('surface_id')
    edge_surface_cell_data.SetNumberOfComponents(1)

    edge_crack_surface_id = vtkIntArray()
    edge_crack_surface_id.SetName('crack_surface_id')
    edge_crack_surface_id.SetNumberOfComponents(2)

    edge_grid.GetCellData().AddArray(edge_surface_cell_data )
    edge_grid.GetCellData().AddArray(edge_crack_surface_id)

    # new element generated
    new_element_grid = vtkUnstructuredGrid()
    new_element_cell_data_0 = vtkIntArray()
    new_element_cell_data_0.SetName('element_id')
    new_element_cell_data_0.SetNumberOfComponents(1)
    new_element_grid.GetCellData().AddArray(new_element_cell_data_0)

    new_element_cell_data_1 = vtkIntArray()
    new_element_cell_data_1.SetName('id')
    new_element_cell_data_1.SetNumberOfComponents(1)
    new_element_grid.GetCellData().AddArray(new_element_cell_data_1)

    new_element_cell_data_2 = vtkIntArray()
    new_element_cell_data_2.SetName('adjacent_element_id')
    new_element_cell_data_2.SetNumberOfComponents(1)
    new_element_grid.GetCellData().AddArray(new_element_cell_data_2)

    new_element_id_generator = new_id_generator()

    # endregion

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

            # TODO vtk_cell? polyhedron?
            # If use copy_vtk_cell, when we check crack angle later,
            # it may generate two polygon without a common edge, WHY?
            # The check angle dihedral is in file NMM.crack_3D.ElementCrack3D.py
            # temp_element_vtk_cell = copy_vtk_cell(temp_element_vtk_cell, element_grid.GetPoints())
            temp_element_vtk_cell = copy_polyhedron(temp_element_vtk_cell, element_grid.GetPoints())

            # debug of vtk_cell.IntersectWithCell()
            # if each_element_id == 3130:
            #     u_grid = vtkUnstructuredGrid()
            #
            #     insert_a_cell_0(u_grid, temp_element_vtk_cell)
            #     insert_a_cell_0(u_grid, initial_crack_polygon)
            #
            #     writer = vtkXMLUnstructuredGridWriter()
            #     writer.SetInputData(u_grid)
            #     writer.SetFileName('log.vtu')
            #     writer.Write()
            #     print(temp_element_vtk_cell.IntersectWithCell(initial_crack_polygon, 0.00001))

            if temp_element_vtk_cell.IntersectWithCell(initial_crack_polygon, 0.00001):
                try:
                    temp_crack_surface_vtk_cell, new_element_cell_grid_0,  new_element_cell_grid_1 = clip_a_vtk_cell(temp_element_vtk_cell, origin_point=origin, normal_vector=normal)
                except AssertionError:
                    continue

                # insert new cell into new_element_grid, two cell
                new_element_id_0 = next(new_element_id_generator)
                # print(new_element_cell_grid_0.GetCell(0).GetCellType())
                new_element_vtk_cell_0 = copy_vtk_cell(new_element_cell_grid_0.GetCell(0), new_element_cell_grid_0.GetPoints())
                insert_a_cell(new_element_grid, new_element_vtk_cell_0)
                set_property(new_element_grid, 'id', new_element_id_0, np.array((new_element_id_0, )))
                set_property(new_element_grid, 'element_id', new_element_id_0, np.array((each_element_id, )))

                new_element_id_1 = next(new_element_id_generator)
                insert_a_cell(new_element_grid, new_element_cell_grid_1.GetCell(0))
                set_property(new_element_grid, 'id', new_element_id_1, np.array((new_element_id_1, )))
                set_property(new_element_grid, 'element_id', new_element_id_1, np.array((each_element_id, )))

                set_property(element_grid, 'sub_element_id', each_element_id, np.array((new_element_id_0, new_element_id_1)))
                set_property(new_element_grid, 'adjacent_element_id', new_element_id_0, np.array((new_element_id_1, )))
                set_property(new_element_grid, 'adjacent_element_id', new_element_id_1, np.array((new_element_id_0, )))

                # insert temp_crack_surface into crack_surface_grid.
                temp_crack_surface_id = crack_surface_grid.GetNumberOfCells()
                # cracked flag: 9 is initial crack
                set_property(element_grid, 'cracked', each_element_id, np.array((9,)))
                set_property(element_grid, 'crack_surface_id', each_element_id, np.array((temp_crack_surface_id, -1)))

                # insert_a_cell(crack_surface_grid, temp_crack_surface_vtk_cell)
                insert_a_cell_0(crack_surface_grid, temp_crack_surface_vtk_cell)
                set_property(crack_surface_grid, 'element_id', temp_crack_surface_id, np.array((each_element_id, )))
                # crackElementId.InsertNextValue(each_id)

                # clip surfaces of the element
                temp_element_surface_list = get_property(element_grid, 'surface_id', each_element_id)
                assert len(temp_element_surface_list) == 4
                crack_edge_id_list = []
                for i, each_surface_id in enumerate(temp_element_surface_list):

                    each_surface_id = int(each_surface_id)
                    cracked = int(get_property(surface_grid, 'cracked', each_surface_id)[0])

                    if cracked == 9:
                        temp_edge_id = int(get_property(surface_grid, 'edge_id', each_surface_id)[0])
                        crack_edge_id_list.append(temp_edge_id)

                        adjacent_crack_surface_id = int(get_property(edge_grid, 'crack_surface_id', temp_edge_id)[0])
                        crack_surface_id = (adjacent_crack_surface_id, temp_crack_surface_id)
                        set_property(edge_grid, 'crack_surface_id', temp_edge_id, crack_surface_id)

                    elif cracked == 0:
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
                        set_property(edge_grid, 'crack_surface_id', temp_edge_id, (temp_crack_surface_id, -1))

                        # crack surface
                        crack_edge_id_list.append(temp_edge_id)
                if len(crack_edge_id_list) == 3:
                    crack_edge_id_list.append(-1)

                # if error happen, maybe crack surface interact with element at the vertex......
                assert len(crack_edge_id_list) == 4

                set_property(crack_surface_grid, 'edge_id', temp_crack_surface_id, crack_edge_id_list)

    def write_vtk_model(vtk_model, vtk_file_name, path):
        crackWriter = vtkXMLUnstructuredGridWriter()
        crackWriter.SetFileName(path + vtk_file_name)
        crackWriter.SetInputData(vtk_model)
        crackWriter.Write()

    write_vtk_model(element_grid, 'manifold_element.vtu', geometry_path)
    write_vtk_model(crack_surface_grid, 'crack_surface.vtu', geometry_path)
    write_vtk_model(surface_grid, 'element_surface.vtu', geometry_path)
    write_vtk_model(edge_grid, 'crack_edge.vtu', geometry_path)
    write_vtk_model(new_element_grid, 'new_element.vtu', geometry_path)
