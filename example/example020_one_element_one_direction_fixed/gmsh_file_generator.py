from NMM.base.VTKBase.test_example import generate_tetrahedron
from NMM.base.VTKBase.write_file import write_file
import os

output_path = './mesh/'
output_path = os.path.abspath(output_path)


_, tetrahedron = generate_tetrahedron()
write_file(tetrahedron, output_path+'/gmsh_file.vtu')

