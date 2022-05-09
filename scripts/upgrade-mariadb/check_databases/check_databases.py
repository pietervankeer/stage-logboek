# imports
import os
import re

# variables
ignored_databases = ["mysql","information_schema", "performance_schema"]
# helper functions
def exec_query(query):
    return os.system("mysql -e " + query)

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

def generate_puppet():
    # TODO
    

# main
os.mkdir("/tmp")
with open("/tmp/tmp_db_info.txt","w") as file
    file.write(
    # charset en collation
    exec_query("select SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME from information_schema.schemata;")
    )
    file.close
with open("/tmp/tmp_lv_size.txt","w") as file
    file.write(
    # lv_size
    exec_query("lvs -o lv_name,lv_size vg_mysql")
    )
    file.close
    
with open("/tmp/tmp_db_info.txt", "r") as db_info, open("/tmp/tmp_lv_size.txt", "r") as lv_size, open("/tmp/db.txt","w") as joined_file
    db_info_lines = filter_dbs(db_info.readlines())
    lv_size_lines = lv_size.readlines()
    
    for db_line in db_info_lines:
        for lv_line in lv_size_lines:
            # note to future self: Goed nakijken wat je aan het doen bent.
            # als db_naam overeenkomt: schrijf alles weg naar joined_file
            str=""
            if re.sub("lv_","",lv_line.split())[0] == db_line.split()[0]:
                str += db_line +" "+ lv_line.split()[1] + "\n"
                joined_file.write(str)
    

    

# check lv in /dev/vg_mysql
# command: lvdisplay /dev/vg_mysql
os.system("lvdisplay /dev/mysql")

# charset en collation
exec_query("select SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME from information_schema.schemata;")

# cleanup
os.removedirs("/tmp")