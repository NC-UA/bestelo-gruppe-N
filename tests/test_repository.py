
import json
from pathlib import Path
import pytest

from bestelo.kunden import Geschaeftskunde, Verein, Privatkunde
from bestelo.repository import Sortiment, KundenRepository
from bestelo.fehler import (
    DatenfehlerError,
    KundeExistiertBereitsError,
    KundeNichtGefundenError,
    ProduktNichtGefundenError,
)

def test_als_dict()->None:
    """Hier prüfen wir ob, Anna richtig gespeichert wurde/wird"""
    anna=Privatkunde(1001, "Anna Mueller", "anna@example.com", 1995, True)
    kundendaten=anna.als_dict()
    assert len(kundendaten)==6
    assert kundendaten["typ"]=="Privatkunde"
    assert kundendaten["kundennummer"]==1001
    assert kundendaten["name"]=="Anna Mueller"
    assert kundendaten["email"]=="anna@example.com"
    assert kundendaten["geburtsjahr"]==1995
    assert kundendaten["stammkunde"] is True

def test_kunden_verwalten(tmp_path:Path)->None:
    """Wir prüfen ob die Funktionen funktionieren wie Hinzufuegen, Suchen, Sortieren und die umrechnung auf die automatische nächste Kundennummer"""
    repository=KundenRepository(tmp_path/"kunden.json")
    anna=Privatkunde(1001, "Anna Mueller", "anna@example.com", 1995)
    verein=Verein(1003,"SV Musterstadt","info@sv-musterstadt.de", "VR 1234")

    assert repository.naechste_kundennummer()==1000

    repository.hinzufuegen(verein)
    repository.hinzufuegen(anna)

    assert repository.alle()==[anna, verein]
    assert len(repository)==2
    assert 1001 in repository
    assert repository.holen(1001) is anna
    assert repository.naechste_kundennummer() ==1004

    with pytest.raises(KundeExistiertBereitsError):
        repository.hinzufuegen(anna)
    with pytest.raises(KundeNichtGefundenError):
        repository.holen(4711)

def test_sichern_und_laden(tmp_path:Path)->None:
    """Prüft ob das laden und speichern unsere 3 obigen Kundentypen"""
    pfad=tmp_path/"kunden.json"
    repository=KundenRepository(pfad)
    anna=Privatkunde(1001, "Anna Mueller", "anna@example.com", 1995, True)
    ben=Geschaeftskunde(1002, "Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "DE123456789")
    verein=Verein(1003,"SV Musterstadt","info@sv-musterstadt.de", "VR 1234")

    kunden=[anna, ben, verein]
    for kunde in kunden:
        repository.hinzufuegen(kunde)

    repository.sichern()
    neues_repository=KundenRepository(pfad)
    anzahl=neues_repository.laden()

    assert anzahl== 3

    for kunde in kunden:
        geladener_kunde=neues_repository.holen(kunde.kundennummer)
        assert type(geladener_kunde) is type(kunde)
        assert geladener_kunde.als_dict() == kunde.als_dict()

def test_fehlende_datei(tmp_path:Path)->None:
    """Beim ersten mal starten der Datei könnte die Kundendatei noch fehlen"""
    repository=KundenRepository(tmp_path/"fehlt.json")
    assert repository.laden()==0

def test_kaputte_datei(tmp_path:Path)->None:
    """Wenn die JASON-Datei kaputt sein sollte, sollte die ursprüngliche Fehlersuche bestehen bleiben"""
    pfad=tmp_path/"kunden.json"
    pfad.write_text("kaputt", encoding="utf-8")
    repository=KundenRepository(pfad)

    with pytest.raises(DatenfehlerError) as fehler:
        repository.laden()
    assert isinstance(fehler.value.__cause__,json.JSONDecodeError)

def test_sortiment()->None:
    """Hier wird geprüft ob die angelegten Datein aus Phase 1 vorhanden sind (6 sollten es sein)"""
    sortiment=Sortiment.aus_csv("bestelo/daten/produkte.csv")
    
    assert len(sortiment)==6
    fachbuch=sortiment.holen("P-1004")
    assert fachbuch.bezeichnung=="Fachbuch Python-Grundlagen"

    artikelnummer=[]
    for produkt in sortiment:
        artikelnummer.append(produkt.artikelnummer)
    assert artikelnummer==sorted(artikelnummer)
    assert list(sortiment)==sortiment.alle()

    with pytest.raises(ProduktNichtGefundenError):
        sortiment.holen("P-9999")