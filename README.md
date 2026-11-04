# Projekt-Bestelo

** Gruppe 1 **

## Projektbeschreibung

Bestelo ist ein Shopsystem, das mit Python entwickelt wird.

Das Programm verwaltet verschiedene Kundentypen, Produkte und Bestellungen. Dabei werden je nach Kundentyp unterschiedliche Rabatte sowie die Mehrwertsteuer berücksichtigt. Außerdem können Produkte aus einer CSV-Datei eingelesen werden.

Ziel ist es, die Programmierung in Python praktisch anzuwenden und die Funktionen mithilfe von pytest zu überprüfen.

## Team
| Name |GitHub-Name | Aufgabe | Verantwortung |
|---|---|---|---|
| Nazar Chaika | NC-UA| Person 1 | Kunde und Privatkunde | Teamleitung | 
| Karen Johanna Cosic | karco96 |Person 2 | Geschaeftskunde, Verein, UML-Diagramm und README|
| Elliot Keil | Elliot-Joshua | Person 3 | Produkt und CSV-Datei |
| Lucca Kloiber | Kloiber | Person 4 | Bestellposition, Bestellung und Integrationstests |

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

## So wird das Projekt gestartet 

Für die Ausführung des Projekts wird eine Python-Installation benötigt. Zur Durchführung der automatisierten Tests wird zusätzlich pytest verwendet.

Die folgenden Befehle werden im Terminal im Hauptverzeichnis des Projekts ausgeführt.

Anwendung starten:

python -m bestelo

Tests ausführen:

python -m pytest

## Ideen für Phase 2

Spendenfunktion: Kunden könnten beim Abschluss einer Bestellung freiwillig einen zusätzlichen Betrag an einen gemeinnützigen Verein spenden.
Bestellhistorie: Kunden könnten ihre bisherigen Bestellungen einsehen und Produkte erneut bestellen.
Gemeinsame Bestellungen: Mehrere Vereinsmitglieder könnten Produkte zusammen bestellen, sodass größere Sammelbestellungen einfacher organisiert werden können.
Spezialisierung auf einen Vereinsshop: Das Shopsystem könnte für Sport- oder Kulturvereine erweitert werden, beispielsweise für den Verkauf von Vereinskleidung und Zubehör


```