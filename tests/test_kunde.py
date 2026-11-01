import pytest
from bestelo.kunden import Kunde, Privatkunde


# Test 1 prüft, ob Name gestrippt wird, sowie ob str() und repr() stimmen.
def test_kundenname():
    anna = Kunde(1001, "  Anna Müller ", "anna@example.com")
    assert anna.name == "Anna Müller"
    assert str(anna) == "Kunde 1001: Anna Müller"
    assert repr(anna) == "Kunde (1001, 'Anna Müller')"

# Test 2 prüft, ob beim Anlegen der ungültigen E-Mail Adresse Value Error ausgelöst wird.
def test_ungueltige_email() -> None:
    #Test ist bestanden, wenn ValueError ausgelöst wird
    with pytest.raises(ValueError):
        Kunde(1001, "  Anna Müller ", "anna.example.com")

# Test 3 prüft, ob beim Ändern der Kundennummer eine AttributeError ausgelöst wird.
# Kundennummer soll nur lesbar sein und darf nicht geändert werden.  
def test_kundennummer_nur_lesbar() -> None:
    anna = Kunde(1001, "  Anna Müller ", "anna@example.com")
    with pytest.raises(AttributeError):
        anna.kundennummer = 5

# Test 4 prüft, ob Geburtsjahr zwischen 1900 und aktuellem Jahr liegt. Wenn nein -> ValueError auslösen. 
def test_privatkunde_geburtsjahr() -> None:
    anna = Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, stammkunde=True)
    assert anna.alter(2026) == 31
    with pytest.raises(ValueError):
        Privatkunde(1001, "Anna Müller", "anna@example.com", 2028, stammkunde=True)

# Test 5 prüft den Rabattsatz für Stammkunde 
def test_rabattsatz_stammkunde() -> None:
    anna = Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, stammkunde=True)
    assert anna.rabattsatz() == 0.02

# Test 6 prüft den Rabattsatz für nicht Stammkunde
def test_rabattsatz_kein_stammkunde() -> None:
    anna = Privatkunde(1001, "Anna Müller", "anna@example.com", 1995, stammkunde=False)
    assert anna.rabattsatz() == 0.0