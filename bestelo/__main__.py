from pathlib import Path
import tempfile
from bestelo.bestellungen import Bestellung
from bestelo.kunden import Geschaeftskunde, Kunde, Privatkunde, Verein 
from bestelo.produkte import Produkt
from bestelo.rabatte import BesterRabatt, KundenRabatt, Mengenrabatt #neu hinzugefügt
from bestelo.repository import KundenRepository, Sortiment
from bestelo.zahlung import Kreditkarte, Rechnung
from bestelo.fehler import BesteloError
from bestelo.warenkorb import Warenkorb


"""diese __main__.py Datei soll man im VS-Code im Termin mit folgendem Befehl ausführen:
python -m bestelo (so steht auch im Skript auf Seite 13).
Wenn man __main__.py über "Run Python File Button startet, dann kommt es zu folgen Fehlermeldung: 
'ModuleNotFoundError: No module named 'bestelo' """

CSV_PFAD=Path(__file__).parent/"daten"/"produkte.csv"

def beleg_drucken(bestellung:Bestellung)->None:
    """Hier wird der vorgegebene Kassenzettel angegeben"""
    rabatt_prozent=round(bestellung.rabattsatz*100)
    print("=" * 50)
    print(f"Bestellung{bestellung.bestellnummer} ({bestellung.status})")
    begruessung=bestellung.kunde.begruessung()
    print(begruessung)
    if not begruessung.endswith("-" * 50):
        print("-" * 50)
    
    for position in bestellung.position:
        produkt=position.produkt
        print(position)
   
    print("-" * 50)
    print(f"Netto: {bestellung.netto_summe:.2f}€")
    print(f"Rabatt{rabatt_prozent}%: {-bestellung.rabatt_betrag:.2f}€")
    print(f"MwSt: {bestellung.mwst_betrag:.2f}€")
    print(f"Brutto: {bestellung.brutto_summe:.2f}€\n")
    print(f"({bestellung.rabattregel.beschreibung()})")

def main()-> None:
    """Hier wird die Demo mit den Produkten, Kunden und Bestellung befüllt"""
    print("Sortiment (nach Preis):")
    sortiment=Sortiment.aus_csv(CSV_PFAD)
    produkte =sortiment.alle()
    produkte.sort()
    for p in produkte:
        print(f"\t{p}")
    print()

    """Hier werden die Kunden angelegt und aufgelistet"""
    anna=Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, True)
    ben=Geschaeftskunde(1002, "Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "DE123456789", zahlungsziel_tage=30)
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
    
    """Hier wird die abgeschlossene Bestellung bezahlt"""
    rechnung=Rechnung(ben.zahlungsziel_tage)
    rechnungsbeleg=bestellung1.bezahlen(rechnung)
    print(rechnungsbeleg)

    """Wir legen 12 mal Wasser in den Einkauskorb"""
    mineralwasser=sortiment.holen("P-1002")
    warenkorb=Warenkorb()
    warenkorb.hinzufuegen(mineralwasser, 12)

    """Alles was im Einkausfkorb liegt wird hier angezeigt"""
    anzahl_produkte=len(warenkorb)
    anzahl_produkte=warenkorb.stueckzahl
    nettosumme=warenkorb.netto
    print(f"Warenkorb: {anzahl_produkte} Produkt(e), {anzahl_produkte} Stück, {nettosumme:.2f} € netto")

    """Hier wird für Anna der Rabattsatz festgelegt"""
    kundenRabatt=KundenRabatt()
    mengenrabatt=Mengenrabatt(ab_stueck=10, satz=0.04)
    rabattregeln=[kundenRabatt, mengenrabatt]
    bester_rabatt=BesterRabatt(rabattregeln)

    """Jetzt aus allem im Einkaufskorb einen Bestellung bauen"""
    annas_bestellung=warenkorb.bestellen(anna, bester_rabatt)
    annas_bestellung.abschliessen()
    beleg_drucken(annas_bestellung)

    """Wenn Anna mit der Karte zahlen sollte(macht Sie)"""
    kreditkarte=Kreditkarte(anna.name, "4111 1111 1111 4242")
    zahlungsbeleg=annas_bestellung.bezahlen(kreditkarte)
    print(zahlungsbeleg)

    try:
        annas_bestellung.hinzufuegen(mineralwasser, 1)
    except BesteloError as fehler:
        print("Fehler: ",fehler)

    """Hier laden wir alle 3 möglichen Kunden in eine temporäre Datei"""
    with tempfile.TemporaryDirectory() as ordner:
        pfad=Path(ordner) / "kunde.json"
        repository=KundenRepository(pfad)

        for kunde in [anna, ben, sv]:
            repository.hinzufuegen(kunde)

        repository.sichern()

        """Hier werden die Daten mit Hilfe von einem 2 Repository zurückgelesen"""
        neues_repository=KundenRepository(pfad)
        anzahl=neues_repository.laden()
        print(f"{anzahl} Kunden wurde gespeichert und geladen")

        geladener_ben=neues_repository.holen(1002)
        print(repr(geladener_ben))

"""Hier wird gesorgt das main ausgeführt wird. """
if __name__=="__main__":
    main()