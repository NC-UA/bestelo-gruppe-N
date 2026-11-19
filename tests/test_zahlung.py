from bestelo.zahlung import Rechnung, Zahlungsmittel
import pytest 
from bestelo.fehler import ZahlungAbgelehntError
from bestelo.zahlung import Rechnung, Kreditkarte, Zahlungsmittel
from bestelo.bestellungen import Bestellung
from bestelo.kunden import Privatkunde
from bestelo.produkte import Produkt
from bestelo.fehler import BestellstatusError

def test_rechnung_ist_zahlungsmittel()-> None:
    rechnung = Rechnung()

    assert isinstance(rechnung, Zahlungsmittel)

def test_rechnung_ueber_5000_euro()-> None:
    rechnung = Rechnung()


    with pytest.raises(ZahlungAbgelehntError):
        rechnung.bezahlen(5000.01)

def test_kreditkarte() -> None:
    karte = Kreditkarte("Anna Müller", "4111 1111 1111 4242")

    assert karte.gebuehr(102.82) == 1.54 

    assert karte.bezahlen(102.82) == (
        "Kreditkarte **** 4242: 104.36 € belastet"

    )

    with pytest.raises(ValueError):
        Kreditkarte("Anna Müller", "1234")


def test_bestellung_nur_einmal_bezahlen() -> None:
    kunde = Privatkunde(1001, "Anna Müller", "anna@example.com", 1995)
    produkt = Produkt("P-1004", "Fachbuch Python-Grundlagen", 24.90, "Bücher")

    bestellung = Bestellung(kunde)
    bestellung.hinzufuegen(produkt)

    # Eine offene Bestellung darf nicht bezahlt werden.
    with pytest.raises(BestellstatusError):
        bestellung.bezahlen(Rechnung())

    # Nach dem Abschließen darf bezahlt werden.
    bestellung.abschliessen()
    bestellung.bezahlen(Rechnung())

    assert bestellung.status == "bezahlt"

    # Eine zweite Zahlung muss abgelehnt werden.
    with pytest.raises(BestellstatusError):
        bestellung.bezahlen(Rechnung())

def test_abgelehnte_zahlung_status_bleibt_abgeschlossen() -> None:
    kunde = Privatkunde(1001, "Anna Müller", "anna@example.com", 1995)
    produkt = Produkt("P-1004", "Fachbuch Python-Grundlagen", 24.90, "Bücher")

    bestellung = Bestellung(kunde)
    bestellung.hinzufuegen(produkt, 200)
    bestellung.abschliessen()

    with pytest.raises(ZahlungAbgelehntError):
        bestellung.bezahlen(Rechnung())

    assert bestellung.status == "abgeschlossen"
