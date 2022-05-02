# MSSQL: logins

[Opdracht](../opdrachten/opdracht-mssql.md)

## Kan windows authentication gebruikt worden?

Ja, Windows auth kan hiervoor gebruikt worden maar dan moet men wel alle bestaande gebruikers gaan converteren naar Windows auth. Echter is het niet mogelijk om bestaande sql logins te converteren naar windows logins maar men moet nieuwe windows logins aanmaken met dezelfde eigenschappen als de bestaande sql logins daarna kan men nieuwe users aanmaken voor die login. Het gebruiken van windows auth is hier niet het probleem maar het probleem ligt bij de jtds driver. Het is niet mogelijk om key-bqsed authenticatie te gaan doen.

### Voordelen

- Je kan dan een gebruiker aanmaken in AD waar niemand het wachtwoord van weet en zo de veiligheid van het systeem verhogen.

### Nadelen

- Het converteren van SQL auth naar Windows auth is niet ondersteund en er zullen dus nieuwe gebruikers moeten aangemaakt worden.
- Bestaande users (sql logins) kunnen niet hermapt worden naar een Windows logins dus we zullen alle logins opnieuw moeten aanmaken.

## Alternatieve authenticatie?

Je kan gebruik maken van de microsoft JDBC driver.

### JDBC voordelen

- Driver van microsoft.

### JDBC nadelen

- Het is niet mogelijk om windows authenticatie te gebruiken als ge vanaf een Linux machine wil connectie maken naar de databank.

## Configuratie/software/drivers?

- <https://www.programcreek.com/2009/08/java-connect-ms-sql-server-using-windows-authentication/>

- Benodigdheden voor het script
  - `SqlServer` module (<https://www.powershellgallery.com/packages/Sqlserver/21.1.18256>)

## Bronnen

- <https://www.razorsql.com/articles/ms_sql_server_jdbc_connect.html>
- <https://newbedev.com/connect-to-sql-server-with-windows-authentication-from-a-linux-machine-through-jdbc>
