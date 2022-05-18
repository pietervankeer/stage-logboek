# check users: are all existing users defined in puppet?

# imports
import os
import pandas as pd
from datetime import date
import yaml
import re

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
        "generated_puppet.txt",
        "w",
    )

    for userrow in users.itertuples():
        strpuppet = (
            userrow[2]
            + ":\n  ensure: present"
            + "\n  password: "
            + userrow[3]
            + "\n  host: "
            + userrow[1]
            + "\n  grants:\n"
        )
        for grantrow in grants.itertuples():
            username = grantrow[1].strip("`")
            if userrow[2] != username or userrow[1] != grantrow[2].strip("`"):
                continue

            # Als de privileges toe te passen zijn op alle db's dan hanteren we een algemene schrijfwijze
            if grantrow[4] == "*.*":
                strpuppet = (
                    strpuppet
                    + "    "
                    + grantrow[1].strip("`")
                    + ":"
                    + "\n      ensure: present"
                    + "\n      db: *"
                    + "\n      privileges:"
                )
            else:
                strpuppet = (
                    strpuppet
                    + "    "
                    + grantrow[1].strip("`")
                    + "@"
                    + grantrow[4].split(".")[0]
                    + ":"
                    + "\n      ensure: present"
                    + "\n      db: "
                    + grantrow[4].split(".")[0]
                    + "\n      privileges:"
                )
            privileges = grantrow[3].split("|")
            privileges.sort()
            strpuppet += "\n      - "
            for privilege in privileges:
                if privileges.index(privilege) == 0:
                    strpuppet += privilege.strip()
                else:
                    strpuppet += ", " + privilege.strip()
            strpuppet += "\n"
        output_file.write(strpuppet)
    output_file.close()


def get_grants(users):

    # Testing purpose
    grant_file = open("show_grants_example.txt", "r")
    return process_grant_input(grant_file.readlines())
    # for user in users.itertuples():
    #    tmp_file = open(
    #        "tmp_users.txt",
    #        "w",
    #    )
    #    tmp_file = exec_query("show grants for " + user[2] + "@" + user[1])
    #    tmp_file.close()
    #    return process_grant_input(tmp_file)


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
            + "\n"
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


def chars_to_str(list):
    # convert unwanted special characted to string
    for line in list:
        y = re.findall("[*][^ ]+", line)
        idx = list.index(line)
        if len(y) > 0:
            list[idx] = re.sub("[*][^ ]+", '"' + y[0] + '"', line)
        elif " * " in line or " % " in line:
            list[idx] = line.replace("*", '"*"\n').replace("%", '"%"\n')
    return list


def compare_puppet():
    # open files
    with open("input_puppet.txt", "r") as input_puppet_file, open(
        "generated_puppet.txt", "r"
    ) as generated_puppet_file:
        # generate tmp files
        tmp_file1 = open("tmp1.txt", "w")
        tmp_file2 = open("tmp2.txt", "w")

        # process tmp files
        input_puppet_lines = input_puppet_file.readlines()
        generated_puppet_lines = generated_puppet_file.readlines()
        input_puppet_lines = chars_to_str(input_puppet_lines)
        generated_puppet_lines = chars_to_str(generated_puppet_lines)
        tmp_file1.writelines(input_puppet_lines)
        tmp_file2.writelines(generated_puppet_lines)
        tmp_file1.close()
        tmp_file2.close()

        tmp_file1 = open("tmp1.txt", "r")
        tmp_file2 = open("tmp2.txt", "r")

        # read yml
        input_puppet = yaml.safe_load(tmp_file1)
        generated_puppet = yaml.safe_load(tmp_file2, Loader=yaml.BaseLoader)

        # remove tmp files

    print(generated_puppet)

    flag = False

    return flag


def generate_output(flag):
    output_file = open("output.txt", "w")

    output_file.write("Report generated on: " + str(date.today()))

    output_file.close


# main
ignore_users = ["root", "backup", "snow_dbdetect"]
users = get_users()
grants = get_grants(users)
generate_puppet(users, grants)
# is_puppet_ok = compare_puppet()
# generate_output(is_puppet_ok)
