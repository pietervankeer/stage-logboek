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
    return os.system("mysql -e " + query)


def get_users():

    # open files
    tmp_file = open(
        "tmp_users.txt",
        "w",
    )
    test_input = open(
        "user_input.txt",
        "r",
    )
    input_lines = test_input.readlines()
    # TODO uncomment test purpose
    # input_lines = exec_query("select user, host from mysql.user;")
    user_lines = []
    # filter usefull lines and prepare for processing
    for line in input_lines:
        if line[:1] != "+":
            line = line.strip("\n").strip("|").replace(" ", "") + "\n"
            if not is_ignored_user(line):
                user_lines.append(line)

    tmp_file.writelines(user_lines)
    tmp_file.close()

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
            if userrow[2] != grantrow[1].strip("`"):
                continue
            # TODO logica goed nakijken.
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
            for grant in grants.itertuples():
                strpuppet += "\t\t\t\t- " + privilege
            strpuppet += "\n"
        output_file.write(strpuppet)
    output_file.close()


def get_grants(users):

    grant_file = open("show_grants_example.txt", "r")

    process_grant_input(grant_file.readlines())

    # for user in users.itertuples():
    #    tmp_file = open(
    #        "tmp_users.txt",
    #        "w",
    #    )
    #    tmp_file = exec_query("show grants for " + user[2] + "@" + user[1])
    #    tmp_file.close()
    #    process_grant_input(tmp_file)


def process_grant_input(grant_input):
    # TODO
    tmp_file = open(
        "tmp_grants.txt",
        "w",
    )
    grant_lines = filter_grant_input(grant_input)

    # process each line so that you get a useabable panda.
    # bron: https://www.geeksforgeeks.org/python-extract-string-between-two-substrings/
    tmp_file.write("user,host,grants,priv_level,grant_option\n")
    for line in grant_lines:
        grant_opt = False
        sub1 = "GRANT "
        sub2 = " ON "
        sub3 = " TO "
        sub4 = " IDENTIFIED BY PASSWORD "
        sub5 = " WITH "
        idx1 = line.index(sub1)
        idx2 = line.index(sub2)
        idx3 = line.index(sub3)
        idx4 = line.index(sub4)
        grants = ""
        priv_level = ""
        user = ""
        # for indexes between sub1 and sub2
        for i in range(idx1 + len(sub1), idx2):
            grants += line[i]
        if "all" in grants:
            grants = ["all"]
        grants = grants.strip().replace(",", "|")

        # for indexes between sub2 and sub3
        for i in range(idx2 + len(sub2), idx3):
            priv_level += line[i]
        priv_level = priv_level.strip(" ")

        if "WITH" not in line:
            # for indexes between sub3 and end of line
            for i in range(idx3 + len(sub3), idx4):
                user += line[i]
        else:
            grant_opt = True
            # for indexes between sub3 and sub4
            idx5 = line.index(sub5)
            for i in range(idx3 + len(sub3), idx4):
                user += line[i]
        user.replace("`", "")

        # write to tmp file
        if grant_opt:
            grant_opt = "Y"
        else:
            grant_opt = "N"
        tmp_file.write(
            user.split("@")[0]
            + ","
            + user.split("@")[1]
            + ","
            + grants
            + ","
            + priv_level
            + ","
            + grant_opt
        )
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


def filter_grant_input(grant_input):
    grant_lines = []
    for line in grant_input:
        # line is not header line or spacer
        if line[:1] != "+" and "Grants for" not in line:
            grant_lines.append(line.strip("\n").strip("|") + "\n")
    return grant_lines


# main
ignore_users = ["root", "backup", "snow_dbdetect"]
users = get_users()
# grants = get_grants(users)

# Testing purpose
grant_file = open("show_grants_example.txt", "r")
process_grant_input(grant_file.readlines())

# generate_puppet(users, grants)
