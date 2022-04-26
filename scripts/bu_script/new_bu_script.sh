#! /bin/bash


set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don’t hide errors within pipes

#----------------------------
# Variables
#----------------------------

# TESTING PURPOSE VARIABLES
# remove after development
CONFIG_bu_root='/home/pieter/bu_dir'
CONFIG_file_cnf="$CONFIG_bu_root/files/cnf_files"
CONFIG_file_db_exclude="$CONFIG_bu_root/files/exclude_db"
CONFIG_file_bu_log="$CONFIG_bu_root/files/bu.log"
CONFIG_file_bu_report="$CONFIG_bu_root/files/bu_report.log"
CONFIG_backup_dir="$CONFIG_bu_root/data"
CONFIG_mail_address="pieter.vankeer@mil.be"
CONFIG_backup_dest="/home/pieter/backup"

# mysql backup user.
CONFIG_mysql_dump_username='backup'
CONFIG_mysql_dump_password='test'
CONFIG_mysql_dump_host='localhost'

CONFIG_mysql_standard_socket='/var/lib/mysql/mysql.sock'

errorflag=0
#----------------------------
# Functions
#----------------------------

# fix_file_format: Make sure file format is LF
fix_file_format(){
    dos2unix "$CONFIG_file_cnf"
    dos2unix "$CONFIG_file_db_exclude"
}

# prepreplog: prepare the report file. (empty file, create header...)
# @args: $CONFIG_file_bu_report
prepreplog(){

    # make sure file is empty
    cat /dev/null > "$1"

    # prepare report file with header
    {
    echo "<----------------Backup server $(hostname) at $(date +%Y-%m-%d)---------------->"
    echo " "
    echo "Backup start at $2 "
    } >> "$1"
}

# initiate_server_backup: start the process to backup the db server.
initiate_server_backup(){
    # test connection
    RC=$(test_server $CONFIG_mysql_standard_socket)
    RC=$?
    
    # test backup destination
    test_backup_dest "$CONFIG_backup_dest"

    # if connection with server was successful (see test_server())
    # then: green light for backup
    # else: do not perform anything.
    if [ $RC -eq 0 ];
    then
        # get all de db's on the server
        ALLDB=$(mysql --user="${CONFIG_mysql_dump_username}" --password="${CONFIG_mysql_dump_password}" --host="${CONFIG_mysql_dump_host}" --socket="$CONFIG_mysql_standard_socket" -B -e "show databases" |grep -v "Database")

        EXCLUDES=$(cat $CONFIG_file_db_exclude)

        # for each dbname in ALLDB: check if not excluded and backup
        # BU=1 means db is not excluded so perform backup.
        # BU=0 means db is excluded so do not backup db
        for dbname in $ALLDB
        do            
            # check if dbname needs to be excluded
            if is_excluded $dbname -eq 0 
            then
                DUMP=$CONFIG_backup_dir'/'$(date +%Y%m%d)'_'$dbname'.sql'
                backup_db $CONFIG_mysql_standard_socket $dbname "$DUMP" > /dev/null
            fi
        done
    fi
}

# test_server: check if connection can be established
# @args: socket to connect to the server.
# @return: exit code of the connection to the server
test_server(){
    # test connection and write errors to report
    mysqlshow --user="${CONFIG_mysql_dump_username}" --password="${CONFIG_mysql_dump_password}" --host="${CONFIG_mysql_dump_host}" --socket="$1" 2>> $CONFIG_file_bu_report
    # was connection successful?
    RC=$?
    if [ $RC -ne 0 ]; then
      errorflag=1
    fi
    return $RC
}

# test_backup_dest: check if backup destination is ready to receive the files.
# @args: destination folder to write backup
test_backup_dest(){
    # Normally you would like to write the backup to a remote server/destination but for testing purposes I keep the backup locally.

    if [ ! -e "$1" ]
    then
        mkdir -p "$1"
    fi
}

# is_excluded: check is dbname is excluded from backup
# @args: dbname
# @return: 1 if excluded, 0 if not excluded
is_excluded(){
    excluded=0
    for exclude in $EXCLUDES
    do
        if [ "$1" = "$(echo "$exclude" | cut -f3 -d'/')" ]
        then
            # db needs te be excluded
            excluded=1
        fi
    done
    return $excluded
}

# backup_db: make backup of specific db
# @args: mysql socket, dbname, place to dump files
backup_db(){
    # record time when db backup started
    BUstart=$(date +%s)

    # write in report
    {
    echo " "
    echo "$dbname"
    } >> $CONFIG_file_bu_report


    mysqldump --user="${CONFIG_mysql_dump_username}" --password="${CONFIG_mysql_dump_password}" --host="${CONFIG_mysql_dump_host}" --socket="$1" --routines --databases "$2" 2>>$CONFIG_file_bu_report | gzip > "$3.gz" 2>> $CONFIG_file_bu_report
    RCbu=$?

    # if db backup failed
    # then: remove files.
    # else: move files to backup destination
    if [ $RCbu -ne 0 ]; then
        rm -f $CONFIG_backup_dir"/*" 2>>  $CONFIG_file_bu_report
        errorflag=1
    else
        move_file "$DUMP.gz" $CONFIG_backup_dest > /dev/null
        RCmove=$?

        # if movefile was successfull
        if [ $RCmove -eq 0 ]; then
            drop_old_backup "$CONFIG_backup_dir/$(date +%Y%m%d)_$dbname.sql.gz"
            RCdrop=$?
            if [ $RCdrop -ne 0 ]; then
                errorflag=1
            fi
        else
            errorflag=1
        fi
            # record time when db backup ended
            BUend=$(date +%s)
            BUdiff=$((BUend - BUstart))
            {
            echo "The backup for $dbname was done in = $(echo - | awk -v "S=$BUdiff" '{printf "%dh:%dm:%ds",S/(60*60),S%(60*60)/60,S%60}')"
            echo " "
            } >> $CONFIG_file_bu_report

    fi
}

# Move file to backup destination server
# @args: file to copy, destination for file
# @return: 0 if value of $RC1 and $RC2 both equal 0, else 1
move_file(){
    cp -r "$1" "$2" 2>>  $CONFIG_file_bu_report
    RC1=$?
    rm -f "$1" 2>>  $CONFIG_file_bu_report
    RC2=$?
    if [ $RC1 -eq 0 ] && [ $RC2 -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# drop old backup in backup destination
# @args: filename of the new backup
# @return: 0 if remove operation was successful, >0 is not succesfull
drop_old_backup(){
    rm -f !"$1" 2>>  $CONFIG_file_bu_report
    RC=$?
    return $RC
}

# process_runtime: calculate runtime and give feedback in report.
# @args: ENDSEC, STARTSEC
process_runtime() {
    # Calculate runtime.
    DIFF=$((ENDSEC - STARTSEC))

    # Write feedback in report.
    echo " " >> "$CONFIG_file_bu_report"
    echo "Backup runtime = $(echo - | awk -v "S=$DIFF" '{printf "%dh:%dm:%ds",S/(60*60),S%(60*60)/60,S%60}')" >> "$CONFIG_file_bu_report"
}

# distribute_backup_feedback: send feedback to the world!
# @args: errorflag (are there errors?)
distribute_backup_feedback(){
    send_mail "$1"

    # Area to expand the distribution of feedback to zabbix,...
}

# send mail
# @args: bu error True or false
#
send_mail(){
    if [ "$1" -eq 0 ]; then
        mail -s "Backup done on $(hostname)" $CONFIG_mail_address < $CONFIG_file_bu_report
    else
        mail -s "Backup error on $(hostname)" $CONFIG_mail_address < $CONFIG_file_bu_report
    fi
}

#----------------------------
# Main
#----------------------------

# make sure file is in right format (CRLF --> LF)
fix_file_format

# record time when backup starts
STARTSEC="$(date +%s)"

# prepare the report file
prepreplog $CONFIG_file_bu_report "$(date '+%Y-%m-%d %T')"

# perform server backup
initiate_server_backup

# record time when backup ends
ENDSEC="$(date +%s)"

# calculate runtime
process_runtime "$ENDSEC" "$STARTSEC"

# append report in bu_log
cat $CONFIG_file_bu_report >> $CONFIG_file_bu_log

# distribute feedback
distribute_backup_feedback $errorflag