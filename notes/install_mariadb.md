# Installeer Mariadb

```bash
sudo dnf/yum install mariadb-server
sudo mysql_install_db
systemctl status mariadb
sudo systemctl start mariadb
sudo mysql_secure_installation
```

## manipuleer mariadb

inloggen:

```sql
mysql -u root -p
```

db maken:

```sql
MariaDB [(none)]> CREATE DATABASE testdb;
MariaDB [(none)]> GRANT ALL ON databank.* TO user@localhost IDENTIFIED BY 'securePassowrd';
```

> Bij het maken van een user, let erop om 'securePassowrd' te vervangen door een goed password.