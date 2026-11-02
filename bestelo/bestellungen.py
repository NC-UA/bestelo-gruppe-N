
from bestelo.produkte import Produkt
from bestelo.kunden import Kunde

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
        f"{self.menge}x {self._produkt.bezeichnung} "
        f"für/je {self._produkt.nettopreis:.2f}€"
        f"= {self.netto:.2f}€"
    )

class Bestellung:
      _nr=1
      def __init__(self, kunde: Kunde) ->None:
            self.nummer= Bestellung._nr
            Bestellung._nr+=1
            self.kunde= kunde
            self.status= 'offen'
            self.position= []

      def hinzufuegen(self, produkt:Produkt, menge: int=1) ->None:
            if self.status !='offen': raise ValueError("Nicht offen")
            for position in self.position:
                if position.produkt==produkt:
                    position.menge+=menge
                    return
            self.position.append(Bestellposition(produkt,menge))
    
      @property
      def netto_summe(self) -> float:
            summe=0
    
            for position in self.position:
                summe+=position.netto
    
            return round(summe,2)
    
      @property
      def brutto_summe(self) -> float:
            return round(self.netto_nach_rabatt+self.mwst_betrag,2)
   
      @property
      def mwst_betrag(self) -> float:
            summe=0
    
            for position in self.position:
                summe+=position.mwst
    
            return round(summe*(1-self.kunde.rabattsatz()),2)
    
      @property
      def rabatt_betrag(self) -> float:
        return round(self.netto_summe*self.kunde.rabattsatz(),2)
    
      @property
      def netto_nach_rabatt(self) -> float:
        return round(self.netto_summe-self.rabatt_betrag,2)

      @property
      def bestellnummer(self) -> str:
            if self.nummer <10:
                return "B-000"+str(self.nummer)
            elif self.nummer <100:
                return "B-00"+str(self.nummer)
            elif self.nummer <1000:
                      return "B-0"+str(self.nummer)
            else:
             return "B-" +str(self.nummer)

      def abschliessen (self) -> None:
          if len (self.position)==0:
              raise ValueError("Bestellung sollte Leer sein")
          self.status='abgeschlossen'
      
      def __len__(self) -> int:
          anzahl=len(self.position)
          return anzahl