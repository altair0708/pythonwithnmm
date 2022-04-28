from NMM.plot.PlotPatchDisplacement import plot_patch_displacement
import sqlite3

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    plot_patch_displacement(database_cursor)
