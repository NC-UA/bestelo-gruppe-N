
from bestelo.produkte import Produkt
from bestelo.kunden import Verein
from bestelo.bestellungen import Bestellung
from bestelo.__main__ import main

def test_vereinsbestellung():
    verein=Verein(1001, "Sportsfreunde", "info@sport.de", "VR 1234")
    saft=Produkt("P-1003", "Orangensaft", 2.80 ,"Getränke") 
    bestellung=Bestellung(verein)
    bestellung.hinzufuegen(saft,24)
    assert bestellung.brutto_summe==75.97

def test_demo_zeigt_bruttosumme(capsys):
    main()
    ausgabe=capsys.readouterr().out
    assert "79.66" in ausgabe