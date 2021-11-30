from NMM.base.ContactWithDatabase import get_one_loop, get_window_size, get_loop_bounds
from shapely.affinity import scale
from itertools import combinations
import sqlite3
import matplotlib.pyplot as plt

database_name = '../data/test.db'
database_connect = sqlite3.connect(database_name)
database_cursor = database_connect.cursor()

# get all loops polygon from database
loop_list = []
for temp_i in range(1, 5):
    loop_polygon_temp, loop_line_temp = get_one_loop(temp_i, database_cursor)
    loop_list.append((temp_i, loop_polygon_temp))
    x, y = loop_polygon_temp.exterior.xy
    plt.plot(x, y)
a = combinations(loop_list, 2)
print(type(a))

# get window size from database
window_bounds = get_window_size(database_cursor)
scale_value = 1.05 + 10 * 0.007 / 0.8
window_bounds = scale(window_bounds, xfact=scale_value, yfact=scale_value)
x, y = window_bounds.exterior.xy
plt.plot(x, y)
plt.show()
