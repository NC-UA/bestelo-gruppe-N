import pytest
from bestelo.rabatte import Rabattregel, Mengenrabatt, BesterRabatt, KundenRabatt
from bestelo.bestellungen import Bestellung, Bestellposition
from bestelo.produkte import Produkt
from bestelo.kunden import Kunde

"""Test 1 prüft, ob die Erstellung eines Objekts der Abstraktklasse Rabattregel verhindert wird"""
def test_rabattregel() -> None:
    with pytest.raises(TypeError):
        Rabattregel()

"""Test 2 prüft, ob die übergebene ungültige Parameter für Mengenrabatt einen ValueError auslösen"""
def test_ungueltige_parameter() -> None:
    with pytest.raises(ValueError):
        Mengenrabatt(ab_stueck=0)

    with pytest.raises(ValueError):
        Mengenrabatt(satz=1)

    with pytest.raises(ValueError):
        Mengenrabatt(satz=-0.1)

"""Test 3 prüft, ob die Bestellung ohne Angabe des Rabatts einen KundenRabatt hat"""
def test_kundenrabatt() -> None:
    kunde = Kunde(1001, "  Anna Müller ", "anna@example.com")
    bestellung = Bestellung(kunde)
    assert isinstance(bestellung.rabattregel, KundenRabatt)