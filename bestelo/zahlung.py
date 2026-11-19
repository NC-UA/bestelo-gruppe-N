from typing import Protocol, runtime_checkable 
from bestelo.fehler import ZahlungAbgelehntError


@runtime_checkable
class Zahlungsmittel(Protocol):
    
    def gebuehr(self, betrag: float) -> float:
        ...

    def bezahlen(self, betrag: float) -> str:
        ...


class Rechnung:
    """Zahlugnsmittel für die Bezahlung per Rechnung."""


    HOECHSTBETRAG: float = 5000.00


    def __init__(self, zahlungsziel_tage: int = 14) -> None:

        if not 0 <= zahlungsziel_tage <= 60:
            raise ValueError("Das Zahlungsziel muss zwischen 0 und 60 Tagen liegen.")

        self.zahlungsziel_tage = zahlungsziel_tage


    def gebuehr(self, betrag: float)-> float:
        """Berechnet die Gebühr für eine Rechnungszahlung."""

        return 0.0 
    
    def bezahlen(self, betrag: float) -> str:
            """Prüft den Rechnungsbetrag und erstellt einen Beleg"""
    
            if betrag > self.HOECHSTBETRAG:
                raise ZahlungAbgelehntError(
                    "Der Rechnungsbetrag überschreitet 5000 Euro."
                )
            return (
                f"Rechnung über {betrag:.2f} €, "
                f"zahlbar innerhalb von {self.zahlungsziel_tage} Tagen"
            )

class Kreditkarte :
        """Zahlungsmittel für die Bezahlung per Kreditkarte."""

        GEBUEHRENSATZ : float = 0.015

        def __init__(self, karteninhaber: str, nummer: str) -> None:
            nummer_ohne_leerzeichen = nummer.replace(" ", "")

            if len(nummer_ohne_leerzeichen) != 16 or not nummer_ohne_leerzeichen.isdigit():
                raise ValueError("Die Kartennummer muss genau 16 Ziffern enthalten.")

            self.karteninhaber = karteninhaber
            self._nummer = nummer_ohne_leerzeichen

        @property
        def maskiert(self) -> str:
            """Gibt nur die letzten vier Ziffern der Kartenummer zurück."""
            return f"**** {self._nummer[-4:]}"

        def gebuehr(self, betrag: float) -> float:
                """Berechnet die Kreditkartngebühr von 1,5 Prozent."""
                return round(betrag * self.GEBUEHRENSATZ, 2)
        
        def bezahlen(self, betrag:float) -> str:
            """Berechnet den Gesamtbetrag und erstellt einen Zahlungsbeleg."""
    
            gesamtbetrag = round(betrag + self.gebuehr(betrag), 2)
            return f"Kreditkarte {self.maskiert}: {gesamtbetrag:.2f} € belastet"

        
