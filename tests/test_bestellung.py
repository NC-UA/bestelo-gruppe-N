
from bestelo.bestellungen import Bestellposition, Bestellung

class TestKunde:
     name="Lucca Kloiber"


class TestProdukt:
      bezeichnung="Kissen"
      nettopreis=10.0
      mwst_satz=0.19
     
def test_bestellnummer():
     Bestellung._nr=1
     erste_bestellung=Bestellung(kunde=TestKunde())
     zweite_bestellung=Bestellung(kunde=TestKunde())
     ergebnis=zweite_bestellung.bestellnummer
     if ergebnis != "B-0002":
      raise AssertionError("Die Bestellnummer sollte B-0002 sein!")

def test_gesamtsumme_netto():
     bestellung=Bestellung(kunde=TestKunde())
     mein_produkt=TestProdukt()
     bestellung.hinzufuegen(mein_produkt, menge=1)
     bestellung.hinzufuegen(mein_produkt, menge=1)

     ergebnis=bestellung.netto_summe

     if ergebnis != 20.0:
      raise AssertionError("Die Bestellsumme sollte bei 20.0 liegen!")

def test_leerer_warenkorb():
      bestellung=Bestellung(kunde=TestKunde())
      ergebnis=Bestellung.netto_summe
      if ergebnis != 0:
         raise AssertionError("Leerer Warenkorb sollte bei 0 stehen")
      
def test_rechnen():
    produkt=TestProdukt()
    position=Bestellposition(produkt,menge=2)

    netto=position.netto
    mwst=position.mwst
    brutto=position.brutto

    if netto != 20.0:
        raise AssertionError("Die Nettobetrag sollte bei 20 liegen!")
    
    if mwst != 3.8:
            raise AssertionError("Der Mwstsatz sollte bei 3.8 liegen!")

    if brutto != 23.8:
            raise AssertionError("Die Bruttobetrag sollte bei 23.8 liegen!")
def test_menge_fehler():
          produkt =TestProdukt()
          position=Bestellposition(produkt,menge=1)

          try:
              position.menge=0
          except ValueError:
               return

          assert False, "Hier sollte ein ValueError stehen"  