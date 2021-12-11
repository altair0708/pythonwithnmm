import sqlite3
from NMM.fem.PatchBase import *

database_name = '../data/test.db'
database_connect = sqlite3.connect(database_name)
database_cursor = database_connect.cursor()

patch_number = get_patch_number(database_cursor)

for each_id in range(1, patch_number + 1):
    id, x, y = get_one_patch(each_id, database_cursor)
    plt.scatter(x, y)

plt.show()

database_connect.close()
