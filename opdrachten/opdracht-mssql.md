# Opdracht: mssql logins

Momenteel connecteren JBoss Application Servers zich met MSSQL Server met SQL logins en dus via SQL server Authentication dit verloopt allemaal via een JTDS driver.

De opdracht is om het volgende te onderzoeken:

- Kan Windows authentication gebruikt worden zodat Jboss can connecteren met key-based auth naar mssql?
- Wat zijn mogelijke alternatieven voor Authenticatie?
  - voor- en nadelen (vooral op vlak van Security en Management)
- Welke configuratie/software/drivers moet er geïnstalleerd worden om dit mogelijk te maken?

## Situatie AS-IS

Momenteel connecteren JBoss Application Servers zich met MSSQL Server met SQL logins en dus via SQL server Authentication dit verloopt allemaal via een JTDS driver.  Echter is het niet mogelijk om hier met key-based authenticatie te gaan werken.

## Doel

Om het systeem veiliger te maken wil de dienst MSSQL overschakelen naar Windows authenticatie bij het inloggen op een databank.

## Plan van aanpak

Ik ga beginnen met mezelf bekend te maken met het onderwerp. Ik ga een virtuele machine vragen waar ik op kan testen. Daarna zal ik een oplossing proberen zoeken op het probleem, en als laatste zal ik deze testen.

## Uitwerking

Ik had een virtuele machine gevraagd die ik kon gebruiken als testomgeving. Blijkbaar is het niet zo simpel om voor mij een virtuele machine te voorzien dus hebben ze mij toegang gegeven op een bestaande databank. Zo had ik een omgeving om dingen te testen. Ik heb een gesprek gehad met Donovan om een oplossing te zoeken op het probleem.

## Eindresultaat

Het is mogelijk om om windows authenticatie te gaan gebruiken voor de JBOSS applicaties, dit kan zelf met dezelfde driver. Maar het is niet onbelangrijk om aandacht te schenken aan het volgende: het wachtwoord van de gebruiker die je in AD aanmaakt zal na een bepaalde tijd moeten veranderd worden (afgedwongen door de policy van AD), dit is een grote administratieve taak als je dit moet doen voor alle servers.

## Business doelstellingen

Het systeem zal veiliger zijn met Windows Auhenticatie omdat er dan gebruikers gebruikt worden die gedefinieerd zijn in Active Directory.
