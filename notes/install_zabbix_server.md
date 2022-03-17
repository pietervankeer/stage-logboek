# Install zabbix server

The purpose of this guide is to install zabbix server with mariadb

First, you need to install the zabbix-server, frontend and agent.  
With Puppet you need to use following syntax:  

```puppet
package { [ 'zabbix-server-mysq', 'zabbix-web-mysql', 'zabbix-apache-conf', 'zabbix-sql-scripts', 'zabbix-selinux-policy', 'zabbix-agent' ](provider=dnf):
  ensure => installed
}
```
