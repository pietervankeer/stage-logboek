#! /bin/bash

# Variables

old_tables="$(cat output_old.txt)"
new_tables="$(cat output_new.txt)"
drop=-1
output="patch_command.txt"


# main 

# create outputfile
if [ ! -e $output ]
then
    touch $output
fi

# empty outputfile
echo "" > $output


# iterate tables and generate sql
for old_table in $old_tables
do
    drop=1
    for new_table in $new_tables
    do
        if [ "$old_table" = "$new_table" ]
        then
            drop=0
        fi
    done
    if [ $drop = 1 ]
    then
        echo "drop table $old_table;" >> $output
    fi
done


