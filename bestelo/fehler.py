class BesteloError(Exception):
    """Basiklasse aller Fehlermeldungen."""


class ZahlungAbgelehntError(BesteloError):
    """Zahlung konnte nicht durchgeführt werden."""


class DatenfehlerError(BesteloError):
    """Die Daten waren nicht richtig eingegeben oder wurden nicht richtig gelesen."""


class KundeNichtGefundenError(BesteloError):
    """Der Kunde konnte nicht gefunden werden."""
    def __init__(self, kundennummer: int) -> None:
        super().__init__(f"Kunde {kundennummer} nicht gefunden")
        self.kundennummer = kundennummer


class KundeExistiertBereitsError(BesteloError):
    """Der Kunde existiert bereits."""
    def __init__(self, kundennummer: int) -> None:
        super().__init__(f"Kunde {kundennummer} existiert bereits")
        self.kundennummer = kundennummer


class ProduktNichtGefundenError(BesteloError):
    """Das Produkt konnte nicht gefunden werden."""
    def __init__(self, artikelnummer: str) -> None:
        super().__init__(f"Produkt {artikelnummer} nicht gefunden")
        self.artikelnummer = artikelnummer


class BestellstatusError(BesteloError):
    """Der Vorgang der passt nicht zum Status."""
    def __init__(self, bestellnummer: str, meldung: str) -> None:
        super().__init__(f"{bestellnummer}: {meldung}")
        self.bestellnummer = bestellnummer


class WarenkorbLeerError(BesteloError):
    """Der Warenkorb ist Leer."""
    def __init__(self) -> None:
        super().__init__("Der Warenkorb ist leer")