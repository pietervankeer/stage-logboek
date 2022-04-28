# check users: are all existing users defined in puppet?

# imports
import os
import pandas as pd

# functions
def is_ignored_user(line):
    # check if user needs to be ignored+
    is_ignored = False
    arr = line.split("|")
    for user in ignore_users:
        if arr[1] == user:
            is_ignored = True
    return is_ignored

def exec_query(query):
    return os.system('mysql -e ' + query)

def get_users():

    # open files
    test_file = open(
        "tmp_users.txt",
        "w",
    )

    input_lines = exec_query "select user, host from mysql.user;"
    user_lines = []
    # filter usefull lines and prepare for processing
    for line in input_lines:
        if line[:1] != "+":
            line = line.strip("\n").strip("|").replace(" ", "") + "\n"
            if not is_ignored_user(line):
                user_lines.append(line)

    test_file.writelines(user_lines)
    test_file.close()

    data = pd.read_csv(
        "tmp_users.txt",
        sep="|",
        header=0,
    )

    # cleanup
    os.remove("tmp_users.txt")

    return data

def generate_puppet(users, grants):
    output_file = open(
        "output.txt",
        "w",
    )

    for userrow in users.itertuples():
        strpuppet = (
            userrow[2]
            + ":\n\tensure: present"
            + "\n\tpassword: "
            + userrow[3]
            + "\n\thost: "
            + userrow[1]
            + "\n\tgrants:\n"
        )
        for grantrow in grants.itertuples():
            if userrow[2] != grantrow[1]
                continue
            #TODO logica goed nakijken.
            strpuppet = (
                    strpuppet
                    + "\t\t"
                    + userrow[2]
                    + "@"
                    + grantrow[2]
                    + ":"
                    + "\n\t\t\tensure: present"
                    + "\n\t\t\tdb:"
                    + grantrow[2]
                    + "\n\t\t\tprivileges:\n"
                )
                for privilege in privileges:
                    strpuppet += "\t\t\t\t- " + privilege
                strpuppet += "\n"
        output_file.write(strpuppet)
    output_file.close()

def get_grants(users):
    for user in users.itertuples():
        tmp_file = open(
        "tmp_users.txt",
        "w",
        )
        tmp_file = exec_query("show grants for " + user[2] + "@" + user[1])
        process_grant_input(tmp_file)
        
        tmp_file.close()

def process_grant_input(grant_input):
    # TODO
    tmp_file = open(
        "tmp_grants.txt",
        "w",
        )
    grant_lines = filter_grant_input(grant_input)
    
    # process each line so that you get a useabable panda.
    # bron: https://www.geeksforgeeks.org/python-extract-string-between-two-substrings/
    tmp_grants.write("user,host,grant,priv_level, grant_option\n")
    for line in grant_lines:
        words = line.split(' ')
        for word in words:
            grant_opt=False
            sub1= "grant"
            sub2="on"
            sub3="to"
            sub4="with"
            idx1=word.index(sub1)
            idx2=word.index(sub2)
            idx3=word.index(sub3)
            idx4=word.index(sub4)
        # for indexes between sub1 and sub2
        for i in range(idx1 + len(sub1), sub2):
            grants+=words[i]
        if "all" in grants:
            grants=["all"]
        grants = grants.replace(" ","").split(,)
        for i in range(idx2 + len(sub2), sub3):
            priv_level+=words[i]
        priv_level = priv_level.strip(" ")
        # for indexes between sub2 and sub3
        if "WITH" not in line:
            for i in range(idx3 + len(sub3), len(line) - 1):
                user+=words[i]
        else
            grant_opt=True
            for i in range(idx3 + len(sub3), sub4):
                user+=words[i]
        user.replace("'", "")
        

        # write to tmp file
        for grant in grants:
            tmp_file.write(user.split("@")[0]+','+user.split("@")[1]+','+grant+","+priv_level+','+ grant_opt)
    tmp_file.close()
    
    # create panda
    data = pd.read_csv(
        "tmp_grants.txt",
        sep=",",
        header=0,
    )
    
    # cleanup
    os.remove("tmp_grants.txt")
    
    return data

def filter_grant_input(grant_input)
    grant_lines=[]
    for line in grant_input:
        # line is not header line or spacer
        if line[:1] != "+" and "Grants for" not in line:
            grant_lines.append(line.strip("\n").strip("|")+"\n")
    return grant_lines
# main
ignore_users = ["root", "backup", "snow_dbdetect"]
users = get_users()
grants = get_grants(users)

#print(grants)
#generate_puppet(users, grants)
