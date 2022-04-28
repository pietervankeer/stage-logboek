#! /bin/bash

# variables

# helper functions
exec_query(){
	mysql -e "$1"
}
# main

databases=$(exec_query "show databases;")

for $db in $databases
do

done

# cleanup

rm -rf databases