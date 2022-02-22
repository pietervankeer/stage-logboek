# Stage logboek: Week 1 (21/02/2022 - 24/02/2022)

## Maandag 21/02/2022

_Eerste stagedag_. Kennismaking met __Tom De Leeuw__, Tom staat in voor het linuxgedeelte.
Laptop ontvangen, vooral gepraat over mogelijkheden van de stage.

Werkwijze voor telewerken:

1. surf naar <https://portal.connect.mil.be> en meld aan met __itsme__
2. Kies voor vpn. Eens de verbinding opstaat kan je beginnen met skype.

## Dinsdag 22/02/2022

_8:00 - 16:00_

Zelfstandig research gedaan naar LVM (Linux Volume manager) --> <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_logical_volumes/index>
Na de research enkele kleine opdrachtjes uitgevoerd op mijn eigen devserver binnen Defensie:
1. Aanmaken logical volume
    - Maak logical volume aan van 300mb
    - mount logical volume op `/var/data01`
    - herstart server en kijk of het nog bestaat.
2. Aanpassen logical volume
    - vergroot logical volume
    - verklein logical volume
3. Volume groups
    - maak 2 volume groups van 100-200mb

Achteraf als afsluiter van de dag moest ik een grafische omgeving installeren op mijn devserver en proberen om via windows rdp de server te kunnen overnemen.

## Woensdag 23/02/2022

## Donderdag 24/02/2022