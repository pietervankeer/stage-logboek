#
# Dit script kan gebruikt worden om sql logins om te zetten naar Windows logins
#

#
# Imports
#

Import-Module -Name SqlServer

#
# Variables
#

# db connection
$Instance_name = "cdcwdtasql1601\mssqltest"
$connection_string = "Data Source=$Instance_name;Integrated Security=True;"

#
# Functions
#

Function Query_Dbserver {
    Param {
        [string]$query
    }

    return Invoke-Sqlcmd -Query $query -ConnectionString $connection_string
}

#
# Main
#

# maak temp table met login namen en per db de username
$sql_loginmapping = Query_Dbserver("

IF OBJECT_ID('#userMappings') IS NULL
BEGIN

	CREATE TABLE #userMappings(
		LoginName varchar(200),
		DBName varchar(50),
		UserName varchar(200),
		AliasName varchar(100)
	)

	insert into #userMappings
	EXEC sp_MSloginmappings
END

select * 
from #userMappings
where LoginName != 'sa'
	and LoginName not like '#%'
	and	LoginName in (
		SELECT name
		FROM sys.sql_logins
	)

")

Write-Host $sql_loginmapping