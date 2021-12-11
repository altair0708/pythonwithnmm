from NMM.contact.ContactWithDatabase import get_one_loop, get_window_size, get_buffer_from_loop, \
    get_loop_number, get_possible_contact_from_loop, get_loop_point_in_area
from shapely.affinity import scale
from itertools import combinations
import sqlite3
import matplotlib.pyplot as plt

step_offset = 0.1
database_name = '../data/test.db'
database_connect = sqlite3.connect(database_name)
database_cursor = database_connect.cursor()

# get window size from database
window_bounds = get_window_size(database_cursor)
scale_value = 1.05 + 10 * 0.007 / 0.8
window_bounds = scale(window_bounds, xfact=scale_value, yfact=scale_value)
win_x, win_y = window_bounds.exterior.xy
# plt.plot(x, y)
# plt.show()


# get all loops polygon from database
loop_list = []
loop_number = get_loop_number(database_cursor)
for temp_i in range(loop_number):
    loop_polygon_temp, loop_line_temp = get_one_loop(temp_i + 1, database_cursor)
    x, y = loop_polygon_temp.exterior.xy
    plt.plot(x, y)
    loop_polygon_buffer = loop_polygon_temp.buffer(step_offset)
    loop_list.append((temp_i + 1, loop_polygon_buffer))
    # x, y = loop_polygon_buffer.exterior.xy
loop_list_C = combinations(loop_list, 2)

# calculate all of the overlap loop group
overlap_loop_id = get_buffer_from_loop(loop_list_C, is_separated=True)
for each_loop_id_group in overlap_loop_id:
    # x, y = each_loop_id_group[2].exterior.xy
    # plt.plot(x, y)
    temp_point_list_1 = get_loop_point_in_area(loop_id=each_loop_id_group[0], area=each_loop_id_group[2], cursor=database_cursor)
    temp_point_list_2 = get_loop_point_in_area(loop_id=each_loop_id_group[1], area=each_loop_id_group[2], cursor=database_cursor)
    # for each_point in temp_point_list_1:
    #     plt.scatter(each_point.x, each_point.y)
    # for each_point in temp_point_list_2:
    #     plt.scatter(each_point.x, each_point.y)
    result = get_possible_contact_from_loop(*each_loop_id_group, cursor=database_cursor)

plt.plot(win_x, win_y)
plt.show()

# # calculate all of the overlap loop group
# overlap_loop_id = []
# for each_group in loop_list_C:
#     if is_two_polygon_overlap(each_group[0][1], each_group[1][1], offset=0.1):
#         overlap_loop_id.append((each_group[0][0], each_group[1][0]))
# print(len(overlap_loop_id))
database_connect.close()
