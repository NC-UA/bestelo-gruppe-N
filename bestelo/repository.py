
import json
from pathlib import Path
from typing import Iterator

from bestelo.kunden import Geschaeftskunde, Verein, Kunde, Privatkunde
from bestelo.produkte import Produkt
from bestelo.fehler import (
    DatenfehlerError,
    KundeExistiertBereitsError,
    KundeNichtGefundenError,
    ProduktNichtGefundenError,
)
"""Wir haben erster alle wichtigen Klassen und die jeweilige Bennenung für die JASON Dateien."""
KUNDENTYPEN={
    "Privatkunde":Privatkunde,
    "Geschaeftskunde":Geschaeftskunde,
    "Verein":Verein,
}

def kunde_aus_dict(daten: dict)->Kunde:
    """Hier sollte aus den vorhandenen Daten eine neue Kundendatei erstellt werden"""
    try:
        if not isinstance(daten,dict):
         raise TypeError("Kundeneintrag=Dictionary")
        kundendaten=daten.copy()
        klassenname=kundendaten.pop("typ")
        kundenklasse=KUNDENTYPEN[klassenname]

        for merkmal in ("stammkunde","gemeinnuetzig"):
         if merkmal in kundendaten:
          wert=kundendaten[merkmal]
          if type(wert)is not bool:
             raise TypeError(f"{merkmal} muss true or false sein")

        for zahlenfeld in ("kundennummer","zahlungsziel_tage","geburtsjahr"):
           if zahlenfeld in kundendaten:
              wert=kundendaten[zahlenfeld]
              if type(wert)is not int:
                 raise TypeError(f"{zahlenfeld} eine ganze Zahl")

        kunde=kundenklasse(**kundendaten)
        return kunde
    except (KeyError, TypeError, ValueError, AttributeError) as fehler:
        raise DatenfehlerError(f"Ungueltige Kundendaten:{fehler}") from fehler

class KundenRepository:
    """Hier sollte der Kunde anhand von seiner einmaligen Kundennummer für JASON als JASON abgespeichert werden"""
    def __init__(self,pfad:str|Path) -> None:
        """Wir merken uns den Pfad der Datei und legen uns {} ein neues Repository an"""
        self._pfad=Path(pfad)
        self._kunden:dict[int,Kunde]={}

    def hinzufuegen(self, kunde:Kunde) -> None:
        """Hier sollte dem Kunden seine Kundennummer zugeteilt werden, wenn dieser noch nicht existiert"""
        kundennummer=kunde.kundennummer
        if kundennummer in self._kunden:
            raise KundeExistiertBereitsError(kundennummer)
        self._kunden[kundennummer]=kunde

    def holen(self, kundennummer:int)->Kunde:
        """gibt den Kunden anhand der Kundennummer wieder"""
        try:
            return self._kunden[kundennummer]
        except KeyError as fehler:
            raise KundeNichtGefundenError(kundennummer) from fehler

    def alle(self) -> list[Kunde]:
        """Jetzt sollten wir anhand der Kundennummer die Kunden aufgelistet bekommen"""
        kunden=[]
        for kundennummer in sorted(self._kunden):
            kunde=self._kunden[kundennummer]
            kunden.append(kunde)
        return kunden

    def naechste_kundennummer(self) -> int:
        """Wenn wir keine Kunden haben eine 1000 wiedergeben, wenn wir einen Kunden(Kundennummer) haben dann die Nummer +1"""
        if len (self._kunden)==0:
            return 1000

        hoechste_kundennummer=max(self._kunden)
        return hoechste_kundennummer+1

    def __len__(self) -> int:
        """Gibt an wie viele Kunden wir haben"""
        return len(self._kunden)

    def __contains__(self, kundennummer: int)->bool:
        """Hier wird kontrolliert ob die verbindung mit dem Repository geklappt hat und die Nummer hinterlegt ist"""
        return kundennummer in self._kunden

    def sichern(self)->None:
        """Hier sollten alle Kunden als Liste wiedergegeben werden (JASON)"""
        kundenliste=[]
        for kunde in self.alle():
            kundendaten=kunde.als_dict()
            kundenliste.append(kundendaten)
                        
        with open(self._pfad, "w", encoding="utf-8") as datei:
            json.dump(kundenliste, datei, ensure_ascii=False, indent=2)

    def laden(self)->int:
        """Hier wird alles aus der JASON-Datei(Kunden) gelesen und deren anzahl wiedergegeben """
        try:
            with open(self._pfad, "r", encoding="utf-8") as datei:
                kundenliste=json.load(datei)
            if not isinstance(kundenliste, list):
                raise ValueError("Hier muss eine Liste stehen")
            
            geladene_kunden: dict[int, Kunde]={}

            for kundendaten in kundenliste:
                kunde=kunde_aus_dict(kundendaten)
                kundennummer=kunde.kundennummer

                if kundennummer in geladene_kunden:
                 raise ValueError(f"Doppelte Kundennummer: {kundennummer}")
                
                geladene_kunden[kundennummer]=kunde
        except FileNotFoundError:
            return 0
        except (OSError, ValueError) as fehler:
            raise DatenfehlerError(f"Ladefehler:{fehler}")from fehler
       
        self._kunden=geladene_kunden
        return len(self._kunden)

class Sortiment:
    """Wir bekommen hier unsere Produkte nach der Artikelnummer sortiert"""
    def __init__(self)->None:
       """Hier legen wir ein leeres Sortiement an, so wie oben beim KundenRespository"""
       self._produkte: dict[str, Produkt]={}

    @classmethod
    def aus_csv(cls, pfad:str|Path)->"Sortiment":
       sortiment=cls()
       produkte=Produkt.aus_csv_datei(str(pfad))
       for produkt in produkte:
          artikelnummer=produkt.artikelnummer
          sortiment._produkte[artikelnummer]=produkt        
       return sortiment

    def holen(self, artikelnummer:str)->Produkt:
        """Hier wird ausgegeben die Produktnummer + dem passendem Produkt aus dem Sortiment"""
        try:
            return self._produkte[artikelnummer]
        except KeyError as fehler:
            raise ProduktNichtGefundenError(artikelnummer) from fehler

    def alle(self)->list[Produkt]:
       """Gibt alle Produkte nach der Artikelnummer sortiert zurück"""
       produkte=[]
       for artikelnummer in sorted(self._produkte):
          produkt=self._produkte[artikelnummer]
          produkte.append(produkt)
       return produkte

    def __len__(self)->int:
     """Gibt zurueck wie viele Produkte wir insgesamt haben"""
     return len(self._produkte)
    def __iter__(self)->Iterator[Produkt]:
     """Wir können mit der for-Schleife die Produkte von uns abrufen"""
     return iter(self.alle())