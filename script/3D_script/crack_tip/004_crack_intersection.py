from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, reference
from vtkmodules.vtkCommonDataModel import vtkTriangle, vtkPolygon, vtkUnstructuredGrid, vtkConvexPointSet, vtkPolyhedron
from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter
from NMM.base.VTKBase import write_file, load_a_grid


def triangulate_2d_unstructured_grid(input_ugrid):
    triangle_filter = vtkDataSetTriangleFilter()
    triangle_filter.SetInputData(input_ugrid)
    triangle_filter.Update()

    output_ugrid = vtkUnstructuredGrid()
    output_ugrid.ShallowCopy(triangle_filter.GetOutput())
    return output_ugrid


if __name__ == '__main__':
    u_grid = load_a_grid('re003_quad_result.vtu')
    result = triangulate_2d_unstructured_grid(u_grid)
    write_file(result, 're004_triangulate.vtu')


