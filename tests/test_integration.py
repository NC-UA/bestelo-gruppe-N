
from bestelo.repository import Sortiment
from bestelo.kunden import Verein
from bestelo.bestellungen import Bestellung
from bestelo.__main__ import main

def test_vereinsbestellung():
    """Hier wird geschaut, was passiert wenn der Verein 24 Säfte kauft, es sollte 75.97 rauskommen"""
    verein=Verein(1001, "Sportsfreunde", "info@sport.de", "VR 1234")
    sortiment=Sortiment.aus_csv("bestelo/daten/produkte.csv")
    saft=sortiment.holen("P-1003")
    bestellung=Bestellung(verein)
    bestellung.hinzufuegen(saft,24)
    assert bestellung.brutto_summe==75.97

def test_demo_zeigt_bruttosumme(capsys):
    """Hier wird geschaut, ob die Demo ohne Probleme läuft und wir als Ausgabe 79.66 bekommen"""
    main()
    ausgabe=capsys.readouterr().out
    assert "79.66" in ausgabe
    assert "Kreditkarte **** 4242: 104.36 € belastet" in ausgabe
    assert "3 Kunden gespeichert und wieder geladen" in ausgabe