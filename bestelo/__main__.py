from pathlib import Path

from bestelo.bestellungen import Bestellung
from bestelo.kunden import Geschaeftskunde, Kunde, Privatkunde, Verein 
from bestelo.produkte import Produkt
from bestelo.rabatte import BesterRabatt, KundenRabatt, Mengenrabatt #neu hinzugefügt


"""Ab hier beginnt Beispielcode, den Person 1 im Teil 2 eingeben kann, um zu prüfen, ob der Code funktioniert"""
wasser = Produkt("P-1002", "Mineralwasser 12 × 1 l", 7.50, "Getränke")
anna = Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, stammkunde=True)

menge = Mengenrabatt(ab_stueck=10, satz=0.04)
party = Bestellung(anna, menge)
party.hinzufuegen(wasser, 12)
print(menge.beschreibung(), "→", party.rabattsatz)
print(party.netto_summe, party.rabatt_betrag, party.mwst_betrag, party.brutto_summe)

beste = BesterRabatt([KundenRabatt(), menge])
klein = Bestellung(anna, beste)
klein.hinzufuegen(wasser, 2)
print(klein.rabattsatz)          # nur 2 Stück → Kundenrabatt 2 %
klein.hinzufuegen(wasser, 10)
print(klein.rabattsatz)          # 12 Stück → Mengenrabatt 4 %
print()         

"""Hier endet der Beispielcode aus Teil 2 für Person 1"""


"""diese __main__.py Datei soll man im VS-Code im Termin mit folgendem Befehl ausführen:
python -m bestelo (so steht auch im Skript auf Seite 13).
Wenn man __main__.py über "Run Python File Button startet, dann kommt es zu folgen Fehlermeldung: 
'ModuleNotFoundError: No module named 'bestelo' """

CSV_PFAD=Path(__file__).parent/"daten"/"produkte.csv"

def beleg_drucken(bestellung:Bestellung)->None:
    """Hier wird der vorgegebene Kassenzettel angegeben"""
    print("=" * 50)
    print(f"Bestellung{bestellung.bestellnummer} ({bestellung.status})")
    print(bestellung.kunde.begruessung())
    
    for position in bestellung.position:
        print(position)

    rabatt_prozent=int(bestellung.kunde.rabattsatz()*100)
    
    print("-" * 50)
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
        print(f"\t{p}")
    print()
    """Hier werden die Kunden angelegt und aufgelistet"""
    anna=Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, True)
    ben=Geschaeftskunde(1002, "Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "DE123456789")
    sv=Verein(1003, "SV Musterstadt", "info@sv-musterstadt.de", "VR 1234")

    for kunde in [anna, ben, sv]:
        rabatt_prozent=int(kunde.rabattsatz()*100)
        print(f"{kunde} - {rabatt_prozent}% Rabatt")
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