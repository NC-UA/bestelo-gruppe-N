from bestelo.produkte import Produkt
import pytest

def test_bruttopreis_berechnen() -> None:
    produkt1 = Produkt("P-1010", "Salzstangen - 500g", 1, "Lebensmittel")
    produkt2 = Produkt("P-1011", "Bananensast 1l", 2, "Getränke")
    assert produkt1.mwst_satz == 0.07
    assert produkt1.bruttopreis == 1.07
    assert produkt2.mwst_satz == 0.19
    assert produkt2.bruttopreis == 2.38

def test_ungueltige_werte() -> None:
    with pytest.raises(ValueError):
        Produkt("B-1012", "Salzstangen - 500g", 1, "Lebensmittel")
    with pytest.raises(ValueError):
        Produkt("P-1013", "Pflaumen 500g", 0, "Lebensmittel")
    with pytest.raises(ValueError):
        Produkt("P-1014", "  ", 3.50, "Lebensmittel")
    with pytest.raises(ValueError):
        Produkt("P-1015", "Cheddar 100g", 2.50, "Hahahahahaha")

def test_csv_zeile_auswerten() -> None:
    zeile = "P-1001;Kaffeebohnen 500 g;8.90;Lebensmittel"
    produkt_zeile = Produkt.aus_csv_zeile(zeile)
    produkt = Produkt("P-1001", "Kaffeebohnen 500 g", 8.90, "Lebensmittel")
    assert produkt.artikelnummer == produkt_zeile.artikelnummer
    assert produkt.bezeichnung == produkt_zeile.bezeichnung
    assert produkt.nettopreis == produkt_zeile.nettopreis
    assert produkt.kategorie == produkt_zeile.kategorie

def test_csv_datei_auswerten() -> None:
    produkte = Produkt.aus_csv_datei("bestelo/daten/produkte.csv")
    assert min(produkte).artikelnummer == "P-1003" 
    assert len(produkte) == 6
