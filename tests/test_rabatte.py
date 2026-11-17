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

"""Test 4 prüft, ob man kein Rabatt (0.0) bekommt, wenn man weniger als 10 Stück bestellt"""
def test_mengenrabatt_bis_10_stueck() -> None:
    kunde = Kunde(1001, "Anna Müller", "anna@example.com")
    produkt = Produkt("P-1002", "Mineralwasser 12 × 1 l", 7.50, "Getränke")

    menge = Mengenrabatt(ab_stueck=10, satz=0.04)
    bestellung = Bestellung(kunde, menge)
    bestellung.hinzufuegen(produkt, 9)

    assert bestellung.rabattsatz == 0.0

"""Test 5 prüft, ob man einen Rabatt von 4 % (also 0.04) bekommt, wenn man ab 10 Stück bestellt"""
def test_mengenrabatt_ab_10_stueck() -> None:
    kunde = Kunde(1001, "Anna Müller", "anna@example.com")
    produkt = Produkt("P-1002", "Mineralwasser 12 × 1 l", 7.50, "Getränke")

    menge = Mengenrabatt(ab_stueck=10, satz=0.04)
    bestellung = Bestellung(kunde, menge)
    bestellung.hinzufuegen(produkt, 12)

    assert bestellung.rabattsatz == 0.04