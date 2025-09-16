import pygmsh
import os

output_path = './mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:
    geom.add_box((-10, -10, -10), (20, 20, 20), mesh_size=3)
    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')
