
from bestelo.produkte import Produkt
from bestelo.kunden import Kunde

class Bestellposition:
    """Hier werden die Position der Bestellung hergestellt"""
    def __init__ (self, produkt: Produkt, menge: int=1) -> None:
     """Hier wird eine Bestellposition mit Menge und Produkt hergestellt"""
     self._produkt = produkt
     self.menge = menge

    @property
    def produkt(self) -> Produkt:
     """Hier wird vom Produkt die Position wiedergegeben"""
     return self._produkt

    @property
    def menge(self) -> int:
     """Hier bekommen wir die aktuelle Menge wieder"""
     return self._menge

    @menge.setter 
    def menge(self, wert:int) -> None:
     """Hier wmuss die Menge min. 1 sein"""
     if not wert >= 1:
        raise ValueError("Menge muss 1 sein")
     self._menge = wert

    @property
    def netto(self) -> float:
     """Hier wird eder Nettopreis der gesamten Bestellung (Position) berechnet"""
     betrag=self._produkt.nettopreis*self.menge
     return round(betrag,2)
    
    @property
    def mwst(self) -> float:
     """Hier wird die Mehrwertsteuer der Bestellung (Position) berechnet"""
     betrag=self.netto*self._produkt.mwst_satz
     return round(betrag,2)

    @property
    def brutto(self) -> float:
     """Hier wird der Bruttopreis der gesamten Bestellung (Position) berechnet"""
     betrag=self.netto+self.mwst
     return round(betrag,2)

    def __str__ (self) -> str:
     """Hier wird dieser kommende Text als print ausgegeben"""
     return(
        f"{self.menge}x {self._produkt.bezeichnung} "
        f"für/je {self._produkt.nettopreis:.2f}€"
        f"= {self.netto:.2f}€"
    )

class Bestellung:
      """Hier wird die komplette Bestellung abgewickelt"""
      _nr=1
      def __init__(self, kunde: Kunde) ->None:
            """Hier wird eine Bestellung angelegt mit einer fortlaufenden Nummer"""
            self.nummer= Bestellung._nr
            Bestellung._nr+=1
            self.kunde= kunde
            self.status= 'offen'
            self.position= []

      def hinzufuegen(self, produkt:Produkt, menge: int=1) ->None:
            if self.status !='offen': raise ValueError("Nicht offen")
            for position in self.position:
                """Hier wird die Menge erhöht oder ein Produkt zur Bestellung hinzugefügt"""
                if position.produkt==produkt:
                    position.menge+=menge
                    return
            self.position.append(Bestellposition(produkt,menge))
    
      @property
      def netto_summe(self) -> float:
            summe=0.0
            """Hier wird eidie Nettosumme aller im Warenkorb liegende Produkte (Postitionen) berechnet"""
            for position in self.position:
                summe+=position.netto
    
            return round(summe,2)
    
      @property
      def brutto_summe(self) -> float:
            """Hier wird die Bruttosumme berechnet (Rabatt(Netto)+Rabatt(MWST))"""
            return round(self.netto_nach_rabatt+self.mwst_betrag,2)
   
      @property
      def mwst_betrag(self) -> float:
            """Hier wird die MWST berechnet plus der Rabatt wird beachtet"""
            summe=0.0
    
            for position in self.position:
                summe+=position.mwst
    
            return round(summe*(1-self.kunde.rabattsatz()),2)
    
      @property
      def rabatt_betrag(self) -> float:
        """Hier wird ein Rabatt aufgrund des Kundenrabattes berechnet"""
        return round(self.netto_summe*self.kunde.rabattsatz(),2)
    
      @property
      def netto_nach_rabatt(self) -> float:
        """Hier wird die Nettosumme mit dem Rabatt wiedergegeben"""
        return round(self.netto_summe-self.rabatt_betrag,2)

      @property
      def bestellnummer(self) -> str:
            """Hier wird die Bestellnummer wiedergegeben"""
            if self.nummer <10:
                return "B-000"+str(self.nummer)
            elif self.nummer <100:
                return "B-00"+str(self.nummer)
            elif self.nummer <1000:
                      return "B-0"+str(self.nummer)
            else:
             return "B-" +str(self.nummer)

      def abschliessen (self) -> None:
          """Hier wird die Bestellung auf abgeschlossen gesetzt"""
          if len (self.position)==0:
              raise ValueError("Bestellung sollte nicht Leer sein")
          self.status='abgeschlossen'
      
      def __len__(self) -> int:
          anzahl=0
          for position in  self.position:
           anzahl +=1
          return anzahl