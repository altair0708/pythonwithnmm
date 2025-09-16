from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkBox
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry, vtkExtractUnstructuredGrid
import numpy as np
import warnings


def extract_cells_in_box(vtk_model: vtkUnstructuredGrid, polygon_grid: vtkUnstructuredGrid):
    assert polygon_grid.GetNumberOfCells() == 1

    # 1. 计算边界框
    print(polygon_grid.GetBounds())
    xmin, xmax, ymin, ymax, zmin, zmax = polygon_grid.GetBounds()

    # 2. 创建 vtkBox
    box = vtkBox()
    box.SetBounds(xmin - 1, xmax + 1, ymin - 1, ymax + 1, zmin - 1, zmax + 1)

    # 3. 使用 vtkExtractGeometry 提取在 box 内部的单元
    extractor = vtkExtractGeometry()
    extractor.SetInputData(vtk_model)
    extractor.SetImplicitFunction(box)
    extractor.ExtractInsideOn()
    extractor.ExtractBoundaryCellsOn()  # 可选：提取边界相交单元
    # extractor.ExtractOnlyBoundaryCellsOn()
    extractor.Update()

    return extractor.GetOutput()

# === 使用示例 ===

# 假设 ug 是你的 vtkUnstructuredGrid，box_pts 是8个点的列表
# box_pts = [(x1,y1,z1), ..., (x8,y8,z8)]
# result = extract_cells_in_box(ug, box_pts)

# 可选保存结果
# writer = vtk.vtkUnstructuredGridWriter()
# writer.SetFileName("selected.vtk")
# writer.SetInputData(result)
# writer.Write()
