# SELinux

Security Enhanced Linux

## Discretionary access control (DAC) vs Mandatory access control (MAC)

### DAC

- ownership + permissions
- gebruikers hebben de mogelijkheid (discretion) om permissies van hun eigen bestanden aan te passen.

Met root-access kan je zo goed als alles doen op het systeem.

### MAC

- Maak een policy die statisch is en waar in staat wie wat kan doen.

voornamelijk 2 soorten policies:

- "targeted" - the default policy
- "mls" - Multi-level/ multi-category security

## Status van SELinux opvragen

```bash
getenforce
sestatus 
```

`ls -lZ files/` om label te bekijken.
`restorecon -rv /var/www/html` om label te restoren.

## selinux enablen

1. zet selinux op permissive
2. maak '.autorelabel' op rootlevel --> `touch /.autorelabel`
3. reboot