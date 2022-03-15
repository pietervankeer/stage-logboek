# Opdracht: buscript.sh

Binnen Defensie gebruikt men een bashscript genaamd `bu_script.sh` om een backup te nemen van de databanken die bestaan op een machine en deze weg te schrijven op het netwerk.  
Ik kreeg de opdracht om dit script te moderniseren. Om de opdracht een beetje te vereenvoudigen moest ik de backup's lokaal wegschrijven.

## Situatie AS-IS

Het script bestaat maar het is verouderd. Met het script is het mogelijk om meerdere instances van Mariadb/mysql te backuppen. Het script is zeer lang en moeilijk leesbaar.

## Doel

- Moderniseer het script
- Maak het script meer flexibel door gebruik te maken van meer variabelen.
- Genereer een rapport van de uitvoering van het script
- Schrijf de backup lokaal weg onder de map `~/backup`

## Plan van aanpak

1. Lees het script door en probeer de denkwijze te begrijpen van de persoon die het script geschreven heeft.
2. Verwijder delen die niet meer van toepassing zijn.
3. Voeg meer commentaar toe aan het script zodat iemand die het script later zal doornemen sneller weet wat er gebeurd.
4. Gebruik meer functies aan zodat het script meer leesbaar wordt.
5. Test het script.

## Uitwerking

Ik ben begonnen met het script door te nemen en de logica proberen te verstaan. Tijdens dat ik dit deed heb ik extra commentaar geschreven om duidelijk te maken wat er juist gebeurde in het script. Na een kort gesprek met Tom hebben we besloten om het script enkel te beperken voor server die maar 1 instance hebben van mariadb/mysql. Hierdoor werd het script al veel meer leesbaar. Door extra hulpfuncties toe te voegen is de leesbaarheid ook verbeterd. Tijdens het testen heb ik er nog enkele bugs uitgehaald maar het script werkt zoals gevraagd.

## Eindresultaat

Het eindresultaat is een script dat makkelijker te lezen/verstaan en flexibel is. Het script gaat een rapport genereren van de uitvoering en de backup was te vinden in de map `~/backup`. Er is mogelijkheid om in te toekomst het script uit te breiden zodat dit een melding gaat genereren in Zabbix (monitoring tool).

## Business doelstellingen

Voor de business was het belangrijk dat het script een moderne update kreeg. Dit was zeker het geval.

## Persoonlijke doelstellingen

Voor mij persoonlijk was dit een geslaagde opdracht. Het script is nu meer flexibel en dit zal er voor zorgen dat men dit in de toekomst nog kan uitbreiden.
