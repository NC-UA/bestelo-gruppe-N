class Produkt:
    """Ein Produkt im shop mit Preis."""
       
    KATEGORIEN = ("Lebensmittel", "Getränke", "Bücher", "Haushalt", "Elektronik", "Sonstiges")
    ERMAESSIGTE_KATEGORIEN = ("Lebensmittel", "Bücher")
    MWST_ERMAESSIGT = 0.07
    MWST_REGULAER = 0.19

    def __init__(self, artikelnummer: str, bezeichnung: str, nettopreis: float,
                 kategorie: str = "Sonstiges"):
        """Legt ein Produkt an und prüft, ob die artikelnummer korrekt formatiert ist. """
        if not(len(artikelnummer) == 6 and artikelnummer.startswith("P-")) and artikelnummer[2:].isdigit():
            raise ValueError("Muss dem Format \"P-1001\" entsprechen")
        self._artikelnummer = artikelnummer
        self.bezeichnung = bezeichnung
        self.nettopreis = nettopreis
        self.kategorie = kategorie

    @property
    def artikelnummer(self) -> str:
         """Gibt die Artikelnummer zurück."""
         return self._artikelnummer

    @property
    def bezeichnung(self) -> str:
        """Gibt die Bezeichnung zurück."""
        return self._bezeichnung

    @bezeichnung.setter
    def bezeichnung(self, wert: str) -> None:
        """Legt die Bezeichnung fest; darf nicht leer sein."""
        wert = wert.strip()
        if not wert:
            raise ValueError("Die Bezeichnung darf nicht leer sein")
        self._bezeichnung = wert

    @property
    def nettopreis(self) -> float:
        """Gibt den Nettopreis zurück."""
        return self._nettopreis

    @nettopreis.setter
    def nettopreis(self, wert: float) -> None:
        """Legt den Nettopreis fest; muss größer als 0 sein."""
        if not(wert > 0):
            raise ValueError("Der Nettopreis muss größer als 0 sein")
        self._nettopreis = round(wert, 2)

    @property
    def kategorie(self) -> str:
        """Gibt die Kategorie zurück."""
        return self._kategorie

    @kategorie.setter
    def kategorie(self, wert: str) -> None:
        """Legt die Kategorie fest; muss in den vordefinierten Kategorien vor kommen."""
        if wert not in Produkt.KATEGORIEN:
            raise ValueError("Kategorie muss in KATEGORIEN vorkommen")
        self._kategorie = wert

    @property
    def mwst_satz(self) -> float:
        """Gibt den Mehrwertsteuersatz zurück; Prüft Ermaessigung."""
        return Produkt.MWST_ERMAESSIGT if self.kategorie in Produkt.ERMAESSIGTE_KATEGORIEN else Produkt.MWST_REGULAER

    @property
    def bruttopreis(self) -> float:
        """Berechnet Bruttopreis."""
        return round(self.nettopreis * (1 + self.mwst_satz), 2)

    def __str__(self) -> str:
        """Gibt einen Text bei print aus."""
        return f"{self.artikelnummer} {self.bezeichnung} – {self.nettopreis:.2f} € netto"

    def __repr__(self) -> str:
        """Gibt einen leserlichen Text für den Entwickler."""
        return f"Produkt({self.artikelnummer!r}, {self.bezeichnung!r}, {self.nettopreis}, {self.kategorie!r})"

    def __eq__(self, other: "Produkt") -> bool:
        """Vergleicht Artikelnummer, ob sie gleich sind."""
        if not isinstance(other, Produkt):
            return NotImplemented
        return self.artikelnummer == other.artikelnummer

    def __lt__(self, other: "Produkt") -> bool:
        """Vergleicht Nettopreiser, ob kleiner."""
        return self.nettopreis < other.nettopreis

    @classmethod
    def aus_csv_zeile(cls, zeile: str) -> "Produkt":
        """Erstellt aus einer Zeile ein neues Produkt."""
        artikelnummer, bezeichnung, nettopreis, kategorie = \
            zeile.strip().split(";")
        return cls(artikelnummer, bezeichnung, float(nettopreis), kategorie)

    @classmethod
    def aus_csv_datei(cls, pfad: str) -> list["Produkt"]:
        """Liest die CSV-Datei ein."""
        with open(pfad, encoding="utf-8") as produkte:
            next(produkte)
            liste_produkte = []
            for produkt in produkte:
                produkt = produkt.strip()
                if not produkt:
                    continue
                liste_produkte.append(cls.aus_csv_zeile(produkt))
            return liste_produkte