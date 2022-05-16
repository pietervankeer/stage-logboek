# imports
import os
import re
import pandas as pd

# variables
ignored_databases = ["mysql", "information_schema", "performance_schema"]

# file names
file_root = "tmp/"
file_name_db_info = "tmp_db_info.txt"
file_name_lv_size = "tmp_lv_size.txt"
file_name_db = "tmp_db.txt"
file_name_output = "output.txt"

# files
file_db_info = None
file_lv_size = None
file_db = None

####
## Dev variables
####
test_file_name_db_info = "test_input_db_info.txt"
test_file_name_lv_size = "test_input_lv_size.txt"

# helper functions
def exec_query(query):
    output = os.popen("mysql -e " + query)
    return output.read()


def is_ignored(database):
    flag = False
    if database in ignored_databases:
        flag = True
    return flag


def filter_dbs(databases_lines):
    for line in databases_lines:
        if is_ignored(line.split()[0]):
            databases_lines[databases_lines.index(line)] = ""
    return databases_lines


def open_file(file_path, is_read):
    try:
        file = open(file_path, "r" if is_read else "w")
        return file
    except FileNotFoundError:
        print("The File '" + file_path + "' was not found.")


def read_input():
    get_charset_collation()
    get_lv_sizes()


def get_charset_collation():
    # open file
    file_db_info = open_file(file_root + file_name_db_info, False)

    output = exec_query(
        "select SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME from information_schema.schemata;"
    )
    # test info
    output_lines = open_file("test_input_db_info.txt", True).readlines()
    for line in output_lines:
        output_lines[output_lines.index(line)] = (" ".join(output.split())).replace(
            " ", ","
        ) + "\n"
    file_db_info.writelines(output_lines)
    # close file
    file_db_info.close()


def get_lv_sizes():
    # open file
    file_lv_size = open_file(file_root + file_name_lv_size, False)
    # output = os.popen("lvs -o lv_name,lv_size vg_mysql")
    # arr_lv_sizes = output.read()
    arr_lv_sizes_lines = open_file("test_input_lv_size.txt", True).readlines()

    for line in arr_lv_sizes_lines:
        if arr_lv_sizes_lines.index(line) == 0:
            arr_lv_sizes_lines[arr_lv_sizes_lines.index(line)] = line.replace(
                "LV", "SCHEMA_NAME"
            )

        arr_lv_sizes_lines[arr_lv_sizes_lines.index(line)] = (
            " ".join(arr_lv_sizes_lines.split())
        ).replace(" ", ",").replace("lv_", "") + "\n"
    # write lines in file
    file_lv_size.writelines(arr_lv_sizes_lines)
    # close file
    file_lv_size.close()


def join_inputs():
    file_db_info = open_file(file_root + file_name_db_info, True)
    file_lv_size = open_file(file_root + file_name_lv_size, True)
    file_db = open_file(file_root + file_name_db, False)

    data1 = pd.read_csv(file_root + file_name_db_info)
    data2 = pd.read_csv(file_root + file_name_lv_size)

    # Join data
    data_joined = pd.merge(data1, data2, on="SCHEMA_NAME", how="left")

    file_db.write(data_joined.to_csv(index=False))
    file_db.close()


def generate_test_output():

    # Open file
    file_output = open_file(file_name_output, False)
    # close file
    file_output.close()


# main

# check if file_root exists
if not os.path.exists(file_root):
    os.mkdir("tmp")

read_input()
join_inputs()

# cleanup
# os.removedirs("/tmp")
