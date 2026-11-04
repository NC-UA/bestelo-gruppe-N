"""from bestelo.kunden import Kunde, Privatkunde

anna = Kunde(1001, "  Anna Müller ", "anna@example.com")
print(anna)
print(repr(anna))
print(anna.begruessung(), anna.rabattsatz())
print(anna == Kunde(1001, "A. Müller", "a.mueller@example.com"))
print(Kunde.ist_gueltige_email("anna-at-example.com"))

try:
    anna.name = " "
except ValueError as fehler:
    print("Fehler:", fehler)


anna = Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, stammkunde=True)
print(anna)
print(repr(anna))
print(anna.alter(2026), anna.rabattsatz())
print(isinstance(anna, Kunde))


diese __main__.py Datei soll man im VS-Code im Termin mit folgendem Befehl ausführen:
python -m bestelo (so steht auch im Skript auf Seite 13, wenn ich das richtig verstanden habe).
Wenn man __main__.py über "Run Python File Button startet, dann kommt es zu folgen Fehlermeldung: 
'ModuleNotFoundError: No module named 'bestelo' """

from bestelo.produkte import Produkt
from bestelo.kunden import Verein,Privatkunde,Geschaeftskunde
from bestelo.bestellungen import Bestellung
from pathlib import Path

CSV_PFAD=Path(__file__).parent/"daten"/"produkte.csv"

def beleg_drucken(bestellung:Bestellung)->None:
    """Hier wird der vorgegebene Kassenzettel angegeben"""
    print(f"Bestellung{bestellung.bestellnummer} ({bestellung.status})")
    print(bestellung.kunde.begruessung())
    
    for position in bestellung.position:
        print(position)

    rabatt_prozent=int(bestellung.kunde.rabattsatz()*100)
    
    print(f"Netto: {bestellung.netto_summe:.2f}€")
    print(f"Rabatt{rabatt_prozent}%: {-bestellung.rabatt_betrag:.2f}€")
    print(f"MwSt: {bestellung.mwst_betrag:.2f}€")
    print(f"Brutto: {bestellung.brutto_summe:.2f}€\n")

def main()-> None:
    """Hier wird die Demo mit den Produkten, Kunden und Bestellung befüllt"""
    print("Sortiment (nach Preis):")
    produkte =Produkt.aus_csv_datei(CSV_PFAD)
    produkte.sort()
    for p in produkte:
        print(p)
    print()
    """Hier werden die Kunden angelegt und aufgelistet"""
    anna=Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, True)
    ben=Geschaeftskunde(1002, "Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "DE123456789")
    sv=Verein(1003, "SV Musterstadt", "info@sv-musterstadt.de", "VR 1234")

    for kunde in [anna, ben, sv]:
        rabatt_prozent=int(kunde.rabattsatz()*100)
        print(f"{kunde}{rabatt_prozent}Rabatt")
    print()
    """Hier sind hier noch leer aber zugeordnet"""
    bestellung1=Bestellung(ben)
    bestellung2=Bestellung(sv)
    """Hier werden die Produkte in einer Schleife gesucht und benannt"""
    for p in produkte:
        if p.artikelnummer=="P-1001":
            bestellung1.hinzufuegen(p,3)
        elif p.artikelnummer=="P-1002":
            bestellung1.hinzufuegen(p,6)
        elif p.artikelnummer=="P-1003":
            bestellung2.hinzufuegen(p,24)
    """Hier wird die Bestellung abgeschlossen und gedruckt"""
    bestellung1.abschliessen()
    beleg_drucken(bestellung1)

    print(f"Bestellung {bestellung2.bestellnummer} ({bestellung2.status}) für {bestellung2.kunde.name}: {bestellung2.brutto_summe:.2f}€ brutto")
"""Hier wird gesorgt das main ausgeführt wird. """
if __name__=="__main__":
    main()