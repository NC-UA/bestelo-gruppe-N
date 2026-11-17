import pytest
from bestelo.rabatte import Rabattregel, Mengenrabatt
from bestelo.bestellungen import Bestellung

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