from NMM.contact.BlockBase import Block, EAB
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import random

block_a = Block()
point_list1 = [[1, 1], [10, 1], [10, 3], [8, 3], [8, 2], [3, 2], [3, 3], [1, 3]]
for i in range(len(point_list1)):
    for j in range(2):
        point_list1[i][j] = point_list1[i][j] + random.uniform(-0.001, 0.001)
temp = point_list1[0]
point_list1.append(temp)
block_a.polygon = Polygon(point_list1)

block_b = Block()
point_list2 = [[1, 0], [2, 1], [0, 1]]
for i in range(len(point_list2)):
    for k in range(2):
        point_list2[i][k] = point_list2[i][k] + random.uniform(-0.001, 0.001)
temp = point_list2[0]
point_list2.append(temp)
block_b.polygon = Polygon(point_list2)

block_a.draw_boundary()
block_b.draw_boundary()
EAB1 = EAB(block_b, block_a)
for i in EAB1.eab:
    i.draw()
plt.show()
print("finished")
