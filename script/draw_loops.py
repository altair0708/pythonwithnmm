from NMM.base.ContactWithDatabase import get_one_loop, get_window_size, is_two_polygon_overlap, get_loop_number
from shapely.affinity import scale
from itertools import combinations
import sqlite3
import matplotlib.pyplot as plt

database_name = '../data/test.db'
database_connect = sqlite3.connect(database_name)
database_cursor = database_connect.cursor()

# get all loops polygon from database
loop_list = []
loop_number = get_loop_number(database_cursor)
for temp_i in range(loop_number):
    loop_polygon_temp, loop_line_temp = get_one_loop(temp_i + 1, database_cursor)
    print(loop_polygon_temp.area)
    loop_list.append((temp_i + 1, loop_polygon_temp))
    loop_polygon_buffer = loop_polygon_temp.buffer(0.1)
    print(loop_polygon_buffer.area)
    x, y = loop_polygon_buffer.exterior.xy
    plt.plot(x, y)
loop_list_C = combinations(loop_list, 2)

# calculate all of the overlap loop group
overlap_loop_id = []
for each_group in loop_list_C:
    if is_two_polygon_overlap(each_group[0][1], each_group[1][1], offset=0.1):
        overlap_loop_id.append((each_group[0][0], each_group[1][0]))
print(len(overlap_loop_id))


# get window size from database
window_bounds = get_window_size(database_cursor)
scale_value = 1.05 + 10 * 0.007 / 0.8
window_bounds = scale(window_bounds, xfact=scale_value, yfact=scale_value)
x, y = window_bounds.exterior.xy
# plt.plot(x, y)
plt.show()
