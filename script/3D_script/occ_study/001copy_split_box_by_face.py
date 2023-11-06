from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BOPAlgo import BOPAlgo_Splitter
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln
from OCC.Extend.TopologyUtils import TopologyExplorer
display, start_display, add_menu, add_function_to_menu = init_display()
point_0 = gp_Pnt(5, 5, 5)
vector_normal = gp_Dir(1, 1, 1)
point_in = gp_Pln(point_0, vector_normal)
face = BRepBuilderAPI_MakeFace(point_in, -10, 10, -10, 10).Face()
box = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
splitter = BOPAlgo_Splitter()
splitter.AddArgument(box)
splitter.AddTool(face)
splitter.Perform()
for shape in TopologyExplorer(splitter.Shape()).solids():
    display.DisplayShape(shape, update=True)
display.DisplayShape(face, update=True, transparency=0.5, color=rgb_color(1, 0.2, 0))
start_display()
