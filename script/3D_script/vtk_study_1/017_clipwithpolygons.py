from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra, vtkImplicitDataSet

points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 0.0, 1.0)
points.InsertNextPoint(1.0, 1.0, 1.0)

# Create the first tetrahedron
tetra1 = vtkTetra()
tetra1.GetPointIds().SetId(0, 0)
tetra1.GetPointIds().SetId(1, 1)
tetra1.GetPointIds().SetId(2, 2)
tetra1.GetPointIds().SetId(3, 3)

tetra1cell = vtkUnstructuredGrid()
tetra1cell.Allocate(1, 1)
tetra1cell.SetPoints(points)
tetra1cell.InsertNextCell(tetra1.GetCellType(), tetra1.GetPointIds())

tetra1_func = vtkImplicitDataSet()
tetra1_func.SetDataSet(tetra1cell)

point = [0.5, 0.5, 0.5]
print(tetra1_func.EvaluateFunction(point))
