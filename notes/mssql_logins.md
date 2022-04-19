# MSSQL: logins

[Opdracht](../opdrachten/opdracht-mssql.md)

## Kan windows authentication gebruikt worden?

Ja, Windows auth kan hiervoor gebruikt worden maar dan moet men wel alle bestaande gebruikers gaan converteren naar Windows auth. Echter is het niet mogelijk om bestaande sql logins te converteren naar windows logins maar men moet nieuwe windows logins aanmaken met dezelfde eigenschappen als de bestaande sql logins daarna kan men nieuwe users aanmaken voor die login.

### Voordelen

- Je kan dan een gebruiker aanmaken in AD waar niemand het wachtwoord van weet en zo de veiligheid van het systeem verhogen.

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
