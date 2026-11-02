
from bestelo.produkte import Produkt

class Bestellposition:
    def __init__ (self, produkt: Produkt, menge: int=1) -> None:
     self._produkt = produkt
     self.menge = menge

    @property
    def produkt(self) -> Produkt:
     return self._produkt

    @property
    def menge(self) -> int:
     return self._menge

    @menge.setter 
    def menge(self, wert:int) -> None:
     if not wert >= 1:
        raise ValueError("Menge muss 1 sein")
     self._menge = wert

    @property
    def netto(self) -> float:
     betrag=self._produkt.nettopreis*self.menge
     return round(betrag,2)
    
    @property
    def mwst(self) -> float:
     betrag=self.netto*self._produkt.mwst_satz
     return round(betrag,2)

    @property
    def brutto(self) -> float:
     betrag=self.netto+self.mwst
     return round(betrag,2)

    def __str__ (self) -> str:
     return(
        f"{self.menge}x {self._produkt.beschreibung} "
        f"für/je {self.produkt.nettopreis:.2f}€"
        f"= {self.netto():.2f}€"
    )

    