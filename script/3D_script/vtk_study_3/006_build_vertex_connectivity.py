from vtkmodules.vtkCommonDataModel import vtkLine
from NMM.base.VTKBase.load_a_grid import load_a_grid


def build_vertex_connectivity(unstructured_grid):
    vertex_neighbors = {}

    num_cells = unstructured_grid.GetNumberOfCells()

    for i in range(num_cells):
        cell = unstructured_grid.GetCell(i)
        if isinstance(cell, vtkLine):
            pt_id0 = cell.GetPointId(0)
            pt_id1 = cell.GetPointId(1)

            # 将两个点互相添加到对方的邻居列表中
            vertex_neighbors.setdefault(pt_id0, []).append(pt_id1)
            vertex_neighbors.setdefault(pt_id1, []).append(pt_id0)

    # 校验每个点是否正好连接两个点（闭合多边形的必要条件）
    for pt_id, neighbors in vertex_neighbors.items():
        if len(neighbors) != 2:
            print(f"Warning: point {pt_id} has {len(neighbors)} neighbors (not 2). This may not be a closed polygon.")

    return vertex_neighbors


# 示例调用
if __name__ == "__main__":
    
    crack_tip = load_a_grid('crack_tip.vtu')
    vertex_dict = build_vertex_connectivity(crack_tip)

    for k, v in vertex_dict.items():
        print(f"Point ID {k}: connected to {v}")
