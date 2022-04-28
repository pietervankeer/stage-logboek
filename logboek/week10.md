# Stage logboek: Week 10 (25/04/2022 - 29/04/2022)

## Maandag 25/04/2022

werkuren: _08:15-16:15_

Contact gehad met Johan en Donovan over de opdracht van mssql. Meer info gezocht over de jtds driver. ook naar de jdbc driver gekeken.

## Dinsdag 26/04/2022

werkuren: _08:15-16:15_

Verder gewerkt aan de oefening van mssql: meer info gezocht over de jtds en jdbc drivers. niet gevonden wat ik wou vinden.

Om mijn gedachten eens te verzetten heb ik nog eens gekeken naar het script `check_users.py` en heb ik de output een aangepast zodat er nu een waarschuwing staat en verder gescrheven aan het stageverslag.

Voor de opdracht High availability voor mariadb: Research gedaan over hoe we in plaats van master-slave naar master-master kunnen gaan.

## Woensdag 27/04/2022

werkuren: _10:00 - 17:30_

Verder gezocht naar een oplossing voor de jtds driver. Steeds niet gevonden, morgen ga ik hierover met Donovan proberen praten om samen een oplossing te zoeken.
Nagedacht over hoe ik een testopstelling ga opzetten voor een master-master opstelling bij de opdracht High availability voor mariadb.

## Donderdag 28/04/2022

werkuren: _8:15 - 16:15_

Fysiek in Peutie.

JTDS driver:
	- Geen opzoekwerk mogelijk want binnen het netwerk van Defensie is het internet nog niet 100% opengesteld voor het personeel.
	
opdracht High availability voor mariadb:
	- Netwerkdiagram aangepast zodat dit een master-master oplossing is. Nog niet getest.
	
opdracht upgrade mariadb:
	- Nagedacht hoe we een script kunnen schrijven die de check voor de databases doet.
	- Check_users. Python show grants uitvoeren voor elke user. <https://codefather.tech/blog/shell-command-python/>
	- Check_users:
		- verder gewerkt aan het script, logica gescrheven om grants uit te lezen rechtstreeks van de db.
		- input veranderd dat het script de users ook rechtstreeks uit de db gaat halen.
