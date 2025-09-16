from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkOBBTree
from vtkmodules.vtkFiltersSources import vtkLineSource


def intersection_with_shell(polydata: vtkPolyData, p1: list, p2: list):
    # 创建一个射线（线段）作为 vtkLineSource
    line_source = vtkLineSource()
    line_source.SetPoint1(p1)
    line_source.SetPoint2(p2)
    line_source.Update()

    # 使用 vtkOBBTree 来进行射线与表面相交检测
    obbTree = vtkOBBTree()
    obbTree.SetDataSet(polydata)
    obbTree.BuildLocator()

    # 准备交点列表
    intersection_points = vtkPoints()
    intersection_points.SetDataTypeToDouble()

    # 检查是否相交
    obbTree.IntersectWithLine(p1, p2, intersection_points, None)
    point_number = intersection_points.GetNumberOfPoints()

    if point_number == 0:
        return False, p2
    elif point_number == 1:
        # 获取第一个交点（如果存在多个，返回第一个）
        return True, intersection_points.GetPoint(0)
    else:
        raise Exception(f'Intersection_number_error!!!: {point_number}')

