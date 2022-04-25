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


def read_input_users(file):

    # open files
    input_file = open(
        r"C:/Users/Pieter/workspaces/stage-logboek/scripts/upgrade-mariadb/check_users/"
        + file,
        "r",
    )
    test_file = open(
        "C:/Users/Pieter/workspaces/stage-logboek/scripts/upgrade-mariadb/check_users/tmp.txt",
        "w",
    )

    input_lines = input_file.readlines()
    user_lines = []
    # filter usefull lines qnd prepare for processing
    for line in input_lines:
        if line[:1] != "+":
            line = line.strip("\n").strip("|").replace(" ", "") + "\n"
            if not is_ignored_user(line):
                user_lines.append(line)

    test_file.writelines(user_lines)
    test_file.close()

    data = pd.read_csv(
        "C:/Users/Pieter/workspaces/stage-logboek/scripts/upgrade-mariadb/check_users/tmp.txt",
        sep="|",
        header=0,
    )

    # cleanup
    os.remove(
        "C:/Users/Pieter/workspaces/stage-logboek/scripts/upgrade-mariadb/check_users/tmp.txt"
    )

    return data


def generate_puppet(users, grants):
    output_file = open(
        "C:/Users/Pieter/workspaces/stage-logboek/scripts/upgrade-mariadb/check_users/output.txt",
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
            if userrow[2] == grantrow[3] and userrow[1] == grantrow[1]:
                privileges = []
                if (
                    grantrow[4] == "Y"
                    and grantrow[5] == "Y"
                    and grantrow[6] == "Y"
                    and grantrow[7] == "Y"
                    and grantrow[8] == "Y"
                    and grantrow[9] == "Y"
                ):

                    privileges.append("ALL")
                else:
                    if grantrow[4] == "Y":
                        privileges.append("SELECT")
                    if grantrow[5] == "Y":
                        privileges.append("INSERT")
                    if grantrow[6] == "Y":
                        privileges.append("UPDATE")
                    if grantrow[7] == "Y":
                        privileges.append("DELETE")
                    if grantrow[8] == "Y":
                        privileges.append("CREATE")
                    if grantrow[9] == "Y":
                        privileges.append("DROP")
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


# main
ignore_users = ["root", "backup", "snow_dbdetect"]
users = read_input_users("user_input.txt")
# grants = read_input_users("grant_input.txt")

print(users)
# generate_puppet(users, grants)
