# MSSQL: logins

[Opdracht](../opdrachten/opdracht-mssql.md)

## Kan windows authentication gebruikt worden?

Ja, Windows auth kan hiervoor gebruikt worden maar dan moet men wel alle bestaande gebruikers gaan converteren naar Windows auth.

### Voordelen

- Je kan dan een gebruiker aanmaken in AD waar niemand het wachtwoord van weet.

### Nadelen

- Het converteren van SQL auth naar Windows auth is niet ondersteund en er zullen dus nieuwe gebruikers moeten aangemaakt worden.
- Bestaande users (sql logins) kunnen niet hermapt worden naar een Windows logins dus we zullen alle logins opnieuw moeten aanmaken.

### Hoe migreren?

- De connectionstring waarmee de applicatie connectie maakt met de databank zal ook aangepast moeten worden.
- Windows login maken en permissies overzetten van oude login via een script?

## Alternatieve authenticatie?

Als je gebruikt maakt van Azure AD dan kan je hier ook aan authenticatie gaan doen.

## Configuratie/software/drivers?

- <https://www.programcreek.com/2009/08/java-connect-ms-sql-server-using-windows-authentication/>

- Benodigdheden voor het script
  - `SqlServer` module (<https://www.powershellgallery.com/packages/Sqlserver/21.1.18256>)
