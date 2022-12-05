import pygmsh
import meshio
import numpy as np

# 构造一个空的几何体数据结构
#
with pygmsh.geo.Geometry() as geom:
    geom.add_rectangle(0.0, 1.0, 0.0, 1.0, 0.0, 0.1)
    mesh = geom.generate_mesh()
#
# 生成网格 mesh, 其具有数据结构:
#   |- mesh.points              # coordinates of nodes (N*3)
#   |- mesh.cells_dict['line']       # mesh edges (N*2)
#   |- mesh.cells_dict['triangle']   # triangles (N*3)
#
#
# 保存数据或打印, 或者提供给其它使用网格的程序, 如有限元等等
# np.savetxt('points.txt', mesh.points)
# np.savetxt('cells.txt', mesh.cells_dict['triangle'])
#
print(mesh.points)
print(mesh.cells_dict['triangle'])
