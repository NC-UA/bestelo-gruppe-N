from bestelo.produkte import Produkt
from bestelo.bestellungen import Bestellung
from bestelo.fehler import ProduktNichtGefundenError, WarenkorbLeerError
from collections.abc import Iterator
from bestelo.kunden import Kunde
from bestelo.rabatte import Rabattregel

class Warenkorb:
    def __init__(self) -> None:
        """Legt den Warenkorb an."""
        self._artikel: dict[Produkt, int] = {}

    def hinzufuegen(self, produkt: Produkt, menge: int = 1) -> None:
        """Fügt ein Produkt dem Warenkorb hinzu."""
        if menge < 1:
            raise ValueError("Menge kann nicht kleiner als 1 sein")
        self._artikel[produkt] = self._artikel.get(produkt, 0) + menge

    def __len__(self) -> int:
        """Gibt die Länge des Warenkorbs aus."""
        return len(self._artikel)

    def __contains__(self, produkt: Produkt) -> bool:
        """Prüft, ob etwas im Warenkorb ist oder nicht."""
        return produkt in self._artikel

    def __iter__(self) -> Iterator[tuple[Produkt, int]]:
        """Liefert Tupel: (Produkt, Menge)."""
        return iter(self._artikel.items())

    def entfernen(self, produkt: Produkt) -> None:
        """Entfernt ein Produkt."""
        if produkt not in self._artikel:
            raise ProduktNichtGefundenError(produkt.artikelnummer)
        del self._artikel[produkt]

    @property
    def stueckzahl(self) -> int:
        """Liefert die insgesamte Stückzahl aller Produkte im Warenkorb."""
        value = 0
        for menge in self._artikel.values():
            value += menge
        return value

    @property
    def netto(self) -> float:
        """Liefert Nettopreis des gesamten Warenkorbs."""
        nettopreis = 0.0
        for produkt, menge in self._artikel.items():
            nettopreis += produkt.nettopreis * menge
        return round(nettopreis, 2)

    def bestellen(self, kunde: Kunde, rabattregel: Rabattregel | None = None) -> Bestellung:
        """Liefert eine Bestellung."""
        if not self._artikel:
            raise WarenkorbLeerError()
        bestellung = Bestellung(kunde, rabattregel)
        for produkt, menge in self._artikel.items():
            bestellung.hinzufuegen(produkt, menge)
        self._artikel.clear()
        return bestellung


