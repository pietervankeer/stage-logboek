# Procedure: Upgrade Mariadb 5.5

This procedure can be used to upgrade Mariadb 5.5 on RHEL 7 to Mariadb 10.6 on RHEL 8

1. Take vmware-snapshot of vm old db
2. Deploy new vm
    - OS: RHEL 8
    - Puppet Modules: mysqldb
3. Validate users
    - Check if all existing users are defined in puppet
4. Validate databases
    - execute following command to check database sizes: `lvs -o lv_name,lv_size vg_mysql`
    - check .ini file for specific config.
5. Create databases and users with grants via puppet
6. Plan a moment for the upgrade
7. Notify the right people "DB will be under maintenance"
8. Freeze the database
    - Stop the application
    - edit firewall so no external connection can be made
9. Export data from old vm
10. Import the data into new vm
11. Notify the right people "db is ready to be used."
12. If go (upgrade works)
    - delete snapchot old vm
    - delete old vm
13. If no go (upgrade failed)
    - restore snapshot old vm
    - delete snapshot old vm
    - delete new vm
