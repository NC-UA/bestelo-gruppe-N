import pytest
from bestelo.kunden import Geschaeftskunde, Verein 

#Test 1 Prüft, ob Umsatzsteuer ID richtig formatiert wird 
def test_ust_id()-> None:
    ben = Geschaeftskunde(1002,"Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "de 123456789")
    assert ben.ust_id == "DE123456789"

#Test 2 prüft, ob eine ungültige Umsatzsteuer ID abgelehnt wird 
def test_ungueltige_ust_id() -> None:
    with pytest.raises(ValueError):
        Geschaeftskunde(1002,"Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "FR123456789")

#TEst 3 prüft, das Zahlugnsziel eines Geschäftskunden.
def test_zahlungsziel()-> None:
   ben = Geschaeftskunde(1002,"Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "DE123456789") 

   assert ben.zahlungsziel_tage == 14 

   with pytest.raises(ValueError):
       ben.zahlungsziel_tage = 90

#Test 4 prüft die Begrüßung, die textausageb und den Rabatt.
def test_geschaeftskunde() -> None:
   ben = Geschaeftskunde(1002,"Ben Schmidt", "ben@schmidt-it.de", "Schmidt IT GmbH", "DE123456789") 

   assert ben.begruessung() =="Sehr geehrte Damen und Herren der Schmidt IT GmbH,"
   assert str(ben) == "Kunde 1002: Schmidt IT GmbH (Ansprechpartner: Ben Schmidt)"
   assert ben.rabattsatz() == 0.03


# Test5 prüft den Rabatt für gemeinnützige und andere Vereine 
def test_verein_rabatt() -> None:
    verein = Verein(1003, "SV Musterstadt", "info@sv-musterstadt.de", "VR 1234", gemeinnuetzig = True)

    assert verein.rabattsatz() == 0.05
    verein.gemeinnuetzig = False 

    assert verein.rabattsatz() == 0.02

# Test 6 prüft, ob eine ungültige Registernummer abgelehnt wird 
def test_ungueltige_registernummer()-> None:
    with pytest.raises(ValueError):
        Verein(1003,"SV Musterstadt", "info@sv-musterstadt.de", "VR1234")

