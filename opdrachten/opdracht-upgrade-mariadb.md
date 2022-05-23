# Opdracht: Upgrade mariadb 5.5 op RHEL 7 naar Mariadb 10.6 op RHEL 8

Tegen 2024 moeten alle dbserver binnen Defensie draaien op Mariadb 10.6 op RHEL 8. Om deze transitie rustig te laten verlopen is er nood aan een procedure die men kan volgen tijdens zo een upgrade van een machine.

## Situatie AS-IS

De dbservers bij Defensie draaien op mariadb 5.5 op RHEL 7.

## Doel

- De dienst Linux heeft als doel om tegen 2024 alle databankservers die mariadb 5.5 op RHEL 7 draaien, te upgraden naar mariadb 10.6 op RHEL 8. Hierdoor is de kans op kwetsbaarheden in het systeem kleiner en verhoogt de veiligheid. Om dit te bereiken is er nood aan een procedure die men kan volgen om een machine te upgraden. De procedure moet aandacht schenken aan volgende punten:

- Het besturingssysteem van de nieuwe machine is Red Hat Enterprise Linux (RHEL) 8
- Er gaat geen data verloren
- De juiste mensen inlichten dat er onderhoud zal doorgevoerd worden op hun dbserver zodat er geen problemen ontstaan.

## Plan van aanpak

Voor deze opdracht zal ik iteratief werken:

- De eerste iteratie zal ik op papier (in grote lijnen) schetsen wat er moet gebeuren.
- De tweede iteratie zal ik dit in een word-document gieten en laten nalezen door Tom
- De derde en volgende iteratie(s) zal ik de procedure meer specifiek maken
- Eens de procedure duidelijk is, ga ik te werk om bepaalde hulpscripts te schrijven. Deze moeten er voor zorgen dat de persoon die de transitie doet zo weinig mogelijk manueel werk heeft.
- schrijf het script om users te checken
- Als laatste zal ik de procedure grondig testen.

## Uitwerking

Nadat de [procedure](../notes/procedure_upgrade_mariadb.md) opgesteld was en nagekeken door Tom ben ik begonnen aan het script [check_users](../scripts/upgrade-mariadb/check_users/check_users.py). Daarna ben ik begonnen aan het script [check_databases](../scripts/upgrade-mariadb/check_databases/check_databases.py)

## Eindresultaat

Ik heb een procedure (zie [procedure](../notes/procedure_upgrade_mariadb.md)) gemaakt met een aantal scripts die men kan gebruiken om enkele zaken na te kijken alvorens men een upgrade zal uitvoeren.

## Business doelstellingen

De doelstellingen zijn behaald. Er is een procedure die men kan volgen tijdens het uitvoeren van een upgrade. Dit zal het werk makkelijker maken voor de mensen die de procedure uitvoeren. Door de upgrade uit te voeren zal de kans op kwetsbaarheden in het systeem dalen.

## Persoonlijke doelstellingen

Ik heb een procedure en een aantal scripts gemaakt. Voor mij is dit een geslaagde opdracht.
