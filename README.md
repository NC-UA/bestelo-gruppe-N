# Projekt-Bestelo
Aufgabe 1: Nazar (NC-UA)

Aufgabe 2: Karen

Aufgabe 3: Elliot

Aufgabe 4: Lucca (Glotz)

Aufgabe 5: Offen

Wir müssen zwischen round und decimal entscheiden, decimal ist laut Foliensatz aber für Phase 2 bestimmt (Für das Runden der Zahlen da wir immer auf die 2 runden sollen).

## UML-Klassendiagramm

```mermaid
classDiagram
    class Kunde {
        +kundennummer: int
        +name: str
        +email: str
        +begruessung() str
        +rabattsatz() float
        +ist_gueltige_email() bool
        +__init__() 
        +__str__() str
        +__repr__() str
        +__eq__() bool

    }

    class Privatkunde {
        +geburtsjahr: int
        +stammkunde: bool
        +alter() int
        +__init__()
        +rabattsatz() float

    }

    Kunde <|-- Privatkunde

    class Geschaeftskunde {
        +firmenname: str
        +ust_id: str
        +zahlungsziel_tage: int
        +begruessung() str
        +rabattsatz() float
        +__str__() str
        +__init__()
    }
    Kunde <|-- Geschaeftskunde

    class Verein {
        +registernummer: str
        +gemeinnuetzig: bool
        +begruessung() str
        +rabattsatz() float 
        +__init__()
    }
    Kunde <|-- Verein 

    class Produkt{
        +KATEGORIEN: tuple
        +ERMAESSIGTE_KATEGORIEN: tuple
        +MWST_ERMAESSIGT: float
        +MWST_REGULAER: float
        +artikelnummer: str
        +bezeichnung: str
        +nettopreis: float
        +kategorie: str
        +mwst_satz: float
        +bruttopreis: float
        +__init__()
        +aus_csv_zeile() Produkt
        +aus_csv_datei() list
        +__str__() str
        +__repr__() str
        +__eq__() bool
        +__lt__() bool
    }

    class Bestellposition {
        +produkt: Produkt
        +menge: int
        +netto: float
        +mwst: float
        +brutto: float
        +__init__()
        +__str__() str

    }
    class Bestellung{
        -_naechste_nummer: int
        +bestellnummer: str
        +kunde: Kunde
        +status: str
        +positionen: list
        +netto_summe: float
        +rabatt_betrag: float
        +netto_nach_rabatt: float 
        +mwst_betrag: float
        +brutto_summe: float
        +__init__()
        +hinzufuegen() None
        +abschliessen() None
        +__len__() int
        +__str__() str

    }

    Bestellung "0..*" -->"1" Kunde : kunde
    Bestellung "1" *-- "0..*" Bestellposition : positionen
    Bestellposition --> Produkt : produkt 

```