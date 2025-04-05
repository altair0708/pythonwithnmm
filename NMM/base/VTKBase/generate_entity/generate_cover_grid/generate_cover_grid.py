from NMM.base.VTKBase.generate_entity.generate_cover_grid.generate_point_grid import generate_point_grid
from NMM.base.VTKBase.generate_entity.generate_cover_grid.generate_wrapped_grid import generate_wrapped_grid
from NMM.base.VTKBase.generate_entity.generate_cover_grid.generate_element_surface import generate_element_surface
from NMM.base.VTKBase.new_a_grid import new_a_grid
from NMM.base.VTKBase.get_a_vtk_cell_grid import get_a_vtk_cell_grid
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell
from NMM.base.CacheBase import relationship_cache
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkFiltersCore import vtkConvertToPolyhedra
from vtkmodules.vtkCommonCore import vtkIdList


# Id information is also generated
def generate_cover_grid(vtk_model: vtkUnstructuredGrid, cover_name: str):
    if 'mathematics_cover' == cover_name:
        return generate_wrapped_grid(vtk_model)
    elif 'mathematics_point' == cover_name:
        return generate_point_grid(vtk_model)
    elif 'manifold_element' == cover_name:
        converter = vtkConvertToPolyhedra()
        converter.SetInputData(vtk_model)
        converter.Update()
        new_grid = converter.GetOutput()

        # new_grid = new_a_grid()
        # for each_cell in range(vtk_model.GetNumberOfCells()):
        #     vtk_cell = get_a_vtk_cell_grid(vtk_model, each_cell, turn_polyhedron=True)
        #     new_grid = insert_a_vtk_cell(vtk_cell, new_grid)

        return new_grid
    elif 'element_surface' == cover_name:
        return generate_element_surface(vtk_model)
    else:
        raise Exception('Cover name error!!!')

