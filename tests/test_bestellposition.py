
from bestelo.bestellposition import Bestellposition

class TestProdukt:
    beschreibung="Kissen"
    nettopreis=10.0
    mwst_satz=0.19

def test_rechnen():
    produkt=TestProdukt()
    position=Bestellposition(produkt,menge=2)

    netto=position.netto
    mwst=position.mwst
    brutto=position.brutto

    if netto != 20.0:
        raise AssertionError("Die Nettobetrag sollte bei 20 liegen!")
    
    if mwst != 3.8:
            raise AssertionError("Der Mwstsatz sollte bei 20 liegen!")

    if brutto != 23.8:
            raise AssertionError("Die Bruttobetrag sollte bei 20 liegen!")

    def test_menge_fehler():
          produkt =TestProdukt()
          position=Bestellposition(produkt,menge=1)

          try:
              position.menge=0
          except ValueError:
               return

          assert False, "Hier sollte ein ValueError stehen"  

    