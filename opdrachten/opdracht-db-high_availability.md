# Opdracht: DB high availability

Onderzoek hoe men binnen Defensie high availability kan implementeren? Als er een db faalt en niet beschikbaar is moet de applicatie zonder problemen verder werken.

## Situatie AS-IS

Binnen Defensie is er momenteel maar 1 databank achter een bepaalde applicatie. Dit zorgt er natuurlijk voor dat als die databank faalt, de applicatie ook niet meer zal werken.

## Doel

Om de kans op het verliezen van data te verkleinen wil men bij Defensie databank replicatie implementeren.

## Plan van aanpak

Voor deze opdracht zal ik iteratief werken:

- De eerste iteratie zal ik op papier (in grote lijnen) schetsen wat er moet gebeuren alsook ideeën opschrijven van productie die men mogelijk kan gebruiken.
- De tweede iteratie zal ik dit in een word-document gieten en laten nalezen door Tom
- ik ga een master-slave opstelling testen.
- ik ga de master-slave opstelling omvormen naar een master-master opstelling.

Nadat het document volledig is ga ik een handleiding maken om dit te implementeren en een eenvoudige opstelling testen met drie servers (twee \gls{db} servers en 1 een proxyserver).

## Uitwerking

Ik heb een installatie handleiding gemaakt om een master-master opstelling op te zetten.

## Eindresultaat

Er is een handleiding gemaakt die men kan volgen om master-master replicatie op te zetten voor een applicatie. Als er 1 server wegvalt dan zal de proxy automatisch schakelen tussen de db servers.

## Business doelstellingen

Er is replicatie tussen de databank servers.

## Persoonlijke doelstellingen

Ik heb bijgeleerd over replicatie tussen databanken en hun verschillende opstellingen.
