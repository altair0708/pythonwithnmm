from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display

display, start_display, _, _ = init_display()
point_0 = gp_Pnt(0, 0, 0)
point_1 = gp_Pnt(1, 1, 1)
display.DisplayShape(point_0)
display.DisplayShape(point_1)
start_display()

