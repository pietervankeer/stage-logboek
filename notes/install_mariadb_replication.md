# MariaDB: Replication installation guide

## Steps

1. Install MariaDB
2. Start and config MariaDB on primary server
3. Start and config MariaDB on replica server
4. Test MariaDB
5. Install MariaDB MaxScale
6. Start and config MariaDB MaxScale
7. Test MariaDB MaxScale

## Install MariaDB

The repository is already there so we just have to install some packages.

```bash
sudo dnf install MariaDB-server MariaDB-backup
```

## Start/config primary server

Edit config file with following:

```cnf
[mariadb]
bind_address = 127.0.0.1
log_bin      = mariadb-bin.log
server_id    = 1
```

> `server_id` is a unique value

Start the dbserver:
> If already running, restart dbserver to apply config

```bash
systemctl enable mariadb --now
```

There should be at least 2 users created:

1. replication user
2. maxsclae user

Create user accounts:
> each account should be created on the master so replication can make these accounts on the slaves.

### replication user

```sql
CREATE USER 'repl'@'localhost' IDENTIFIED BY 'test';
```

Grant required privileges.

```sql
GRANT REPLICATION SLAVE,
   REPLICATION CLIENT
ON *.* TO repl@'%';
```

### maxscale user

```sql
CREATE USER 'maxs'@'localhost' IDENTIFIED BY 'test';
```

Grant required privileges.

```sql
GRANT SHOW DATABASES ON *.* TO 'mxs'@'192.0.2.%';

GRANT SELECT ON mysql.columns_priv TO 'mxs'@'192.0.2.%';

GRANT SELECT ON mysql.db TO 'mxs'@'192.0.2.%';

GRANT SELECT ON mysql.proxies_priv TO 'mxs'@'192.0.2.%';

GRANT SELECT ON mysql.roles_mapping TO 'mxs'@'192.0.2.%';

GRANT SELECT ON mysql.tables_priv TO 'mxs'@'192.0.2.%';

GRANT SELECT ON mysql.user TO 'mxs'@'192.0.2.%';
```

## Start/config replica server

Edit config file with following:

```cnf
[mariadb]
bind_address = 127.0.0.1
log_bin      = mariadb-bin.log
server_id    = 2
```

> `server_id` is a unique value

### Start replication

```sql
START SLAVE;
```

```sql
SHOW SLAVE STATUS;
```

## Test replication

<https://mariadb.com/docs/deploy/topologies/primary-replica/enterprise-server-10-3/test-es/>

## Install MaxScale

<https://mariadb.com/docs/deploy/topologies/primary-replica/enterprise-server-10-3/install-mxs/>

## Config MaxScale

<https://mariadb.com/docs/deploy/topologies/primary-replica/enterprise-server-10-3/config-mxs/>

## Test MaxScale

<https://mariadb.com/docs/deploy/topologies/primary-replica/enterprise-server-10-3/test-mxs/>