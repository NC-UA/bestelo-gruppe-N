
from bestelo.bestellungen import Bestellposition, Bestellung

class TestKunde:
     """Dummy-Kunde für Testzwecke, Ergebnis = 0"""
     name="Lucca Kloiber"
     def rabattsatz(self):
          return 0.0

class TestProdukt:
      """Dummy-Produkt für Rechnungzwecke"""
      bezeichnung="Kissen"
      nettopreis=10.0
      mwst_satz=0.19
     
def test_bestellnummer():
     """Man schaut ob die Bestellnummer richtig angezeigt und hochzählt wird"""
     """Immer auf 1 zurück, damit man keine Falsche Nummer bekommt """
     Bestellung._nr=1
     """Die 2 Bestellung sollen zeigen ob wir automatisch weiterzählen"""
     erste_bestellung=Bestellung(kunde=TestKunde())
     zweite_bestellung=Bestellung(kunde=TestKunde())
     ergebnis=zweite_bestellung.bestellnummer
     if ergebnis != "B-0002":
      """Haben wir als ERgebnis nicht B-0002 bekommen wir einen Fehler"""
      raise AssertionError("Die Bestellnummer sollte B-0002 sein!")

def test_gesamtsumme_netto():
     """Hiermit sollte geprüft werden ob die Nettosumme der Produkte richtig berechnet werden"""
     bestellung=Bestellung(kunde=TestKunde())
     mein_produkt=TestProdukt()
     """Als Kontrolle legen wir daher 2 Produkte einzeln an"""
     bestellung.hinzufuegen(mein_produkt, menge=1)
     bestellung.hinzufuegen(mein_produkt, menge=1)

     ergebnis=bestellung.netto_summe
     """Wir sollten als Zahl eine 20 herausbekommen da wir 2*10 haben"""
     if ergebnis != 20.0:
      raise AssertionError("Die Bestellsumme sollte bei 20.0 liegen!")

def test_leerer_warenkorb():
      """Hier wird wiedergegeben was passiert, wenn der Warenkorb leer ist"""
      """Wir lesen die Bestellung aus obwohl nichts drinnen steht"""
      bestellung=Bestellung(kunde=TestKunde())
      ergebnis=bestellung.netto_summe
      """Leerer Warenkorb = 0"""
      if ergebnis != 0:
         raise AssertionError("Leerer Warenkorb sollte immer bei 0 stehen")
      
def test_rechnen():
    """Hier wird kontrolliert ob alles richtig (netto....)"""
    produkt=TestProdukt()
    """Wir nehmen hier als Startmenge die 2"""
    position=Bestellposition(produkt,menge=2)

    netto=position.netto
    mwst=position.mwst
    brutto=position.brutto
    """Rechnung 2*10"""
    if netto != 20.0:
        raise AssertionError("Die Nettobetrag sollte bei 20 liegen!")
    
    if mwst != 3.8:
            raise AssertionError("Der Mwstsatz sollte bei 3.8 liegen!")
    """Gesamtsumme von Netto und MWST = 20+3,8 =23,8"""
    if brutto != 23.8:
            raise AssertionError("Die Bruttobetrag sollte bei 23.8 liegen!")
    
def test_menge_fehler():
          """Wir schauen was passiert, wenn wir eine 0 als Menge angeben"""
          produkt =TestProdukt()
          position=Bestellposition(produkt,menge=1)

          try:
              """Wir versuchen hier die Menge von 1 auf die 0 zu setzen"""
              position.menge=0
          except ValueError:
               """Finale Ausgabe"""
               return
          """Wenn der Vorgang nicht vorher beendet wurde, sollten Sie diese Meldung sehen"""
          assert False, "Hier sollte ein ValueError stehen"  