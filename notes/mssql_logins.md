# MSSQL: logins

[Opdracht](../opdrachten/opdracht-mssql.md)

## Kan windows authentication gebruikt worden?

Ja, Windows auth kan hiervoor gebruikt worden maar dan moet men wel alle bestaande gebruikers gaan converteren naar Windows auth. Echter is het niet mogelijk om bestaande sql logins te converteren naar windows logins maar men moet nieuwe windows logins aanmaken met dezelfde eigenschappen als de bestaande sql logins daarna kan men nieuwe users aanmaken voor die login. Het gebruiken van windows auth is hier niet het probleem maar het probleem ligt bij de jtds driver. Het is niet mogelijk om key-based authenticatie te gaan doen.

___Voordelen___

- Je kan gebruikers gaan maken in AD en die gebruiken om connectie te maken met de db.

___Nadelen___

- Het converteren van SQL auth naar Windows auth is niet ondersteund en er zullen dus nieuwe gebruikers moeten aangemaakt worden.
- Bestaande users (sql logins) kunnen niet hermapt worden naar een Windows logins dus we zullen alle logins opnieuw moeten aanmaken.

## Conclusie

Het is mogelijk om om windows authenticatie te gaan gebruiken voor de JBOSS applicaties, maar het is niet onbelangrijk om aandacht te schenken aan het volgende. Het wachtwoord van de gebruiker die je in AD aanmaakt zal na een bepaald tijd moeten veranderd worden (afgedwongen door de policy van AD), dit is een grote administratieve taak als je dit moet doen voor alle servers.

### Single sign-on

### JDBC voordelen

- Driver van microsoft.

### JDBC nadelen

- Het is niet mogelijk om windows authenticatie te gebruiken als ge vanaf een Linux machine wil connectie maken naar de databank.

## Configuratie/software/drivers?

- <https://www.programcreek.com/2009/08/java-connect-ms-sql-server-using-windows-authentication/>

## Bronnen

- <https://www.razorsql.com/articles/ms_sql_server_jdbc_connect.html>
- <https://newbedev.com/connect-to-sql-server-with-windows-authentication-from-a-linux-machine-through-jdbc>

- <https://www.progress.com/blogs/how-to-securely-access-data-on-sql-server#:~:text=There%20are%20essentially%20three%20methods%20used%20for%20authentication,that%20the%20server%20maintains%2C%20a%20connection%20is%20allowed>
