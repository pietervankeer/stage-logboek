# imports
import os

# variables
ignored_databases = ["mysql","information_schema", "performance_schema"]
# helper functions
def exec_query(query):
    return os.system("mysql -e " + query)


# main

# cleanup
