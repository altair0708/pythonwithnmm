import pygmsh
import os

output_path = './mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:

    # 大块体
    box = geom.add_box([0, 0, 0], [6, 20, 20], mesh_size=1.0)

    # 裂纹切口（两个小 box）
    # cut1 = geom.add_box([0, 18, 9.5], [6, 2, 1])
    # cut2 = geom.add_box([0, 0, 9.5], [6, 2, 1])
    #
    # geom.boolean_difference(box, [cut1, cut2])

    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')

# with pygmsh.occ.Geometry() as geom:
#     poly = geom.add_polygon(
#         [
#             [0, 0, 0],
#             [0, 20, 0],
#
#             [0, 20, 9.5],
#             [0, 18, 9.5],
#
#             [0, 18, 10.5],
#             [0, 20, 10.5],
#
#             [0, 20, 20],
#             [0, 0, 20],
#
#             [0, 0, 10.5],
#             [0, 2, 10.5],
#
#             [0, 2, 9.5],
#             [0, 0, 9.5]
#         ],
#         mesh_size=2,
#     )
#     geom.extrude(poly, (6, 0, 0), num_layers=3)
#     mesh = geom.generate_mesh()
