import pygmsh
import os

output_path = '../mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:
    # geom.add_cylinder((0, 0, 0), (2, 0, 0), 10, mesh_size=1)
    geom.add_box((0, 0, 0), (1, 10, 2), mesh_size=0.5)
    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')
