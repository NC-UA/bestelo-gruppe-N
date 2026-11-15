from abc import ABC, abstractmethod

class Rabattregel(ABC):
    @abstractmethod
    def rabattsatz(self, bestellung: float) -> float:
        """Rabattsatz zwischen 0.0 und 1.0 für diese Bestellung"""
        pass

    @abstractmethod
    def beschreibung(self) -> str:
        """Kurzer Text für den Beleg wird ausgegeben"""
        pass

    def rabatt_betrag(self, bestellung: float) -> float:
        return round(bestellung.netto_summe * self.rabattsatz(bestellung), 2)


class KundenRabatt(Rabattregel):
    """Kundenrabatt"""
    def rabattsatz(self, bestellung: float) -> float:
         return bestellung.kunde.rabattsatz()

    def beschreibung(self) -> str:
        return "Kundenrabatt"

class Mengenrabatt(Rabattregel):
    """Mengenrabatt ab 10 Stück"""
    def __init__(self, ab_stueck=10, satz=0.04) -> float:
        if ab_stueck < 1 or not 0 <= satz < 1:
            raise ValueError
        else:
            self.ab_stueck = ab_stueck
            self.satz = satz

    def rabattsatz(self, bestellung: float) -> float:
        if bestellung.stueckzahl >= self.ab_stueck:
            return self.satz
        else:
            return 0.0

    def beschreibung(self) -> str:
        return "Mengenrabatt ab 10 Stück"


class BesterRabatt(Rabattregel):
    """Berechnet den besten Rabatt aus Kundenrabatt und Mengenrabatt """
    def __init__(self, regeln: list[Rabattregel]) -> None:
        if not regeln:
            raise ValueError("Die Rabattliste darf nicht leer sein")
        else:
            self.regeln = regeln

    def rabattsatz(self, bestellung: float) -> float:
        return max(regel.rabattsatz(bestellung) for regel in self.regeln)

    def beschreibung(self) -> str:
        return "Bester Rabatt aus: " + ", ".join(regel.beschreibung() for regel in self.regeln)