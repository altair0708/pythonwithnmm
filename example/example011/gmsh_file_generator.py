import pygmsh
import os

output_path = './mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:
    geom.add_box((-5, 0, 0), (10, 1, 3), mesh_size=0.4)
    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')
