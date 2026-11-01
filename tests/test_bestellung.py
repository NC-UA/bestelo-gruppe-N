
from bestelo.kunden import Kunde
from bestelo.bestellposition import Bestellposition
from bestelo.bestellungen import Bestellung

class TestKunde:
    pass

class TestProdukt:
    nettopreis=10.0
    mwst_satz=0.10

def test_bestellnummer():
 bestellungen=Bestellung(nummer=2, kunde=TestKunde())
 ergebnis=bestellungen.bestelnummer()
 if ergebnis != "0002":
    raise AssertionError("Die Bestellnummer sollte 0002 sein!")

def test_gesamtsumme_netto():
   bestellungen=Bestellung(nummer=1, kunde=TestKunde())
   produkt=TestProdukt()

   position1=Bestellposition(produkt,menge=1)
   position2=Bestellposition(produkt,menge=1)

   bestellungen.position_hinzufügen(position1)
   bestellungen.position_hinzufügen(position2)

   ergebnis=bestellungen.gesamtSumme_netto()

   if ergebnis != 20.0:
      raise AssertionError("Die Bestellsumme sollte bei 20.0 liegen!")

   def test_leerer_warenkorb():
      bestellung=Bestellung(nummer=2, kunde=TestKunde())
      ergebnis=Bestellung.gesamtSumme_netto
      if Ergebnis != 0:
         raise AssertionError("Leerer Warenkorb sollte bei 0 stehen")