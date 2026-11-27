
from fastapi.testclient import TestClient
from bestelo import api
import pytest
from pathlib import Path
from bestelo.kunden import Geschaeftskunde
from bestelo.repository import KundenRepository

client=TestClient(api.app)

def test_produkte_anzeigen()->None:
    """Wir prüfen wir ob die 6 Produkte und die einzelnen Angaben zum Kaffe stimmen"""
    antwort=client.get("/produkte")
    assert antwort.status_code==200

    produkte=antwort.json()
    assert len(produkte)==6

    kaffee=produkte[0]
    assert len(kaffee)== 5
    assert kaffee["artikelnummer"]== "P-1001"
    assert kaffee["bezeichnung"]== "Kaffeebohnen 500 g"
    assert kaffee["kategorie"]== "Lebensmittel"
    assert kaffee["nettopreis"]== 8.90
    assert kaffee["bruttopreis"]== 9.52

def test_kunde_unbekannt()->None:
    """Wir schauen wir, das der StatusCode und der Fehlertext vom Kunde (4711) zusammenpasst"""
    antwort=client.get("/kunden/4711")
    assert antwort.status_code==404

    fehlermeldung=antwort.json()
    assert len(fehlermeldung)==1
    assert fehlermeldung["detail"]=="Kunde 4711 nicht gefunden"

def test_kunde_anzeigen()->None:
    """Hier schauen wir ob der Kunde (1002) die Schmidt IT GmbH ist"""
    antwort=client.get("/kunden/1002")
    assert antwort.status_code==200

    kunde=antwort.json()
    assert kunde["kundennummer"]==1002
    assert kunde["name"]=="Ben Schmidt"
    assert kunde["firmenname"]=="Schmidt IT GmbH"

def 