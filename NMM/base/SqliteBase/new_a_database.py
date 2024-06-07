import sqlite3
import os


def new_a_database(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    with sqlite3.connect(file_name) as connection:
        pass
