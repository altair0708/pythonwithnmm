import pygmsh
import os

output_path = './mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:
    # geom.add_cylinder((0, 0, 0), (6, 0, 0), 10, mesh_size=1.5)
    # geom.add_box(x0=(0, 0, 0), extents=(4, 20, 9), mesh_size=1)
    # geom.add_box(x0=(0, 2, 9), extents=(4, 16, 2), mesh_size=1)
    # geom.add_box(x0=(0, 0, 11), extents=(4, 20, 9), mesh_size=1)
    # mesh = geom.generate_mesh()

    poly = geom.add_polygon(
        [
            [0, 0, 0],
            [0, 20, 0],

            [0, 20, 9.5],
            [0, 18, 9.5],

            [0, 18, 10.5],
            [0, 20, 10.5],

            [0, 20, 20],
            [0, 0, 20],

            [0, 0, 10.5],
            [0, 2, 10.5],

            [0, 2, 9.5],
            [0, 0, 9.5]
        ],
        mesh_size=2,
    )
    geom.extrude(poly, (6, 0, 0), num_layers=3)
    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')
