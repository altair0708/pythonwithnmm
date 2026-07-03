import pygmsh
import os

output_path = './mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:
    geom.add_box((-1, -1, -1), (2, 2, 2), mesh_size=0.2)
    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')
