# Linux ACL

Er zijn 2 soorten acl's in Linux:

- Access ACL
    - geeft access naar files and mappen
- Default ACL
    - kan gebruikt worden met mappen maar geeft de permissies door naar onderliggende kinderen.

Krijg info over acl met command: `getfacl`.  
Maak een acl aan met commando: `setfacl`.

## Access ACL

Add permission for user: `setfacl -m "u:user:permissions" /path/to/file`

Add permission for group: `setfacl -m "g:group:permissions" /path/to/file `

### Demo

```bash
mkdir test
# geef user "pieter" alle rechten.
setfacl -m "u:pieter:rwx" test/
# geef owning group enkel read rechten.
setfacl -m "g::r--" test/
# geef user "jan" geen toegang
setfacl -m "u:jan:---" test/
```

## Default ACL

Add permission for user: `setfacl -m "d:u:user:permissions" /path/to/file`

Add permission for group: `setfacl -m "d:g:group:permissions" /path/to/file `

### Demo

```bash
mkdir test
# geef user "pieter" alle rechten.
setfacl -m "d:u:pieter:rwx" test/
# geef owning group enkel read rechten.
setfacl -m "d:g::r--" test/
# geef user "jan" geen toegang
setfacl -m "d:u:jan:---" test/