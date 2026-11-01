from datetime import date

class Kunde:
    def __init__(self, kundennummer: int, name: str, email: str) -> None:
        #dieser Block prüft, ob Kundennummer kleiner als 1000 ist. Wenn ja -> ValueError, 
        # wenn nein -> wird der Wert als gültige Kundennummer gespeichert
        if kundennummer < 1000:
            raise ValueError("Fehler: Kundennummer darf nicht kleiner als 1000 sein!")
        else:
            self._kundennummer = kundennummer

        self.name = name
        self.email = email

    @property #Kundennummer wird nur lesend gemacht...keine Setter-Methode
    def kundennummer(self) -> int:
        return self._kundennummer

    @property
    def name(self) -> str:
        return self._name
    
    #Name wird durch Setter-Methode definiert. Wenn es keinen Namen gibt (Name ist "leer") -> ValueError,
    # ansonsten wird der Name als gültige Kundenname gespeichert 
    @name.setter 
    def name(self, kundenname: str) -> None:
        if not kundenname.strip(): #entfernt Leerzeichen von beiden Seiten und prüft,  
            raise ValueError("Name darf nicht leer sein") #ob ein Text vorhanden ist
        else:
            self._name = kundenname.strip()

    #durch @staticmethod wird festgelegt welche Kriterien soll eine gültige E-Mail Adresse entsprechen.
    @staticmethod
    def ist_gueltige_email(email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1] #prüft, ob @ in E-Mail vorkommt 
                                                            #und ob es . nach dem @ vorkommt
    @property #Setter-Methode für E-Mail
    def email(self) -> str:
        return self._email

    @email.setter #prüft, ob angegebene E-Mail den Anforderugen von ist_gueltige_email entspricht
    def email(self, adresse: str) -> None:
        if not self.ist_gueltige_email(adresse):
            raise ValueError("Fehler: Diese E-Mail Adresse ist ungültig")
        else:
            self._email = adresse

    def begruessung(self) -> str: #Der Kunde wird begrüßt 
        return f"Hallo {self.name}!"

    def rabattsatz(self, rabatt: float = 0.0) -> float: #Rabattsatz standartmäßig auf 0.0 setzen. 
        return rabatt                                   #später wird er von anderen Kundenklassen überschrieben. 

    def __str__(self) -> str: # __str__ macht die Ausgabe von Kundeninformation für Menschen lesbar
        return f"Kunde {self.kundennummer}: {self.name}"

    def __repr__(self) -> str: #__repr__ ist für Entwickler hilfreich
        return (f"Kunde ({self.kundennummer!r}, {self.name!r})")

    def __eq__(self, other: object) -> bool: # gibt True zurück, wenn Kundennummern gleich sind,
        if not isinstance(other, Kunde):     #ansonsten gibt False zurück 
            return NotImplemented
        else:
            return self.kundennummer == other.kundennummer

 
class Privatkunde(Kunde):
    def __init__(self, kundennummer: int, name: str, email: str, geburtsjahr: int,
                 stammkunde: bool = False) -> None:
        super().__init__(kundennummer, name, email)
        self.geburtsjahr = geburtsjahr
        self.stammkunde = stammkunde


    @property
    def geburtsjahr(self) -> int:
        return self._geburtsjahr
    
    #prüft das angegebene Geburtsjahr. Wenn es kleiner als 1900 oder größer als aktuelles Jahr ist,
    #wird ValueError ausgelöst, ansonsten wird der Wert in der Variable self._geburtsjahr gespeichert. 
    @geburtsjahr.setter 
    def geburtsjahr(self, geburtstag: int) -> None:
        aktuelles_jahr = date.today().year
        if geburtstag < 1900 or geburtstag > aktuelles_jahr:
            raise ValueError
        else:
            self._geburtsjahr = geburtstag

    def alter(self, stichjahr: int | None = None) -> int:
        if stichjahr is None: #stichjahr holt sich das aktuelle Jahr, solange kein Jahr angegeben ist
            stichjahr = date.today().year
        return stichjahr - self._geburtsjahr #hier findet die Berechnung des Alters eines Kundens statt

    def rabattsatz(self) -> float:
        if self.stammkunde:
            return super().rabattsatz() + 0.02 # Stammkunden erhalten 2 % Rabatt. 
        else:                                  # Rabattsatz-Funktion aus Kunde wird hier überschrieben
            return super().rabattsatz()        #Kein Stammkunde -> kein Rabatt

    def __repr__(self):
        return f"Privatkunde ({self.kundennummer!r}, {self.name!r})"

class Geschaeftskunde(Kunde):
    """ stellt einen Geschäftskunde mit Firmenangaben dar """
    def __init__(self,kundennummer: int, name: str, email: str, firmenname: str, ust_id: str, zahlungsziel_tage: int = 14 )-> None:
        """ Initialisiert einen geschäftskunden mit seinen Angaben """
        super().__init__(kundennummer, name, email)
        self.firmenname = firmenname
        self.ust_id = ust_id
        self.zahlungsziel_tage = zahlungsziel_tage


    @property
    def firmenname(self)-> str: 
        """gibt den gespeicherten Firmennamen zurück"""
        return self._firmenname

    @firmenname.setter
    def firmenname(self, firmenname: str)-> None:
        """ Prüft und speichert den Firmennamen """
        if not firmenname.strip():
            raise ValueError("Eingabe darf nicht leer sein") 
        
        else:
    
            self._firmenname = firmenname.strip()

    @property
    def ust_id(self)-> str: 
        """gibt die gespeicherte Umsatzsteuer ID zurück"""

        return self._ust_id

    @ust_id.setter
    def ust_id(self, ust_id: str)-> None:
        """prüft und speichert eine gültige Umsatzsteuer ID"""


        ust_id = ust_id.replace(" ","") # Entfernung der Leerzeichen
        ust_id = ust_id.upper() # Alle Buchstaben werden Groß geschrieben

        if len(ust_id) != 11: # Prüft ob die länge falsch ist 
            raise ValueError ("Falsche Länge")
        
        if not ust_id.startswith("DE"): #Prüft ob die Umsatzsteuer ID mit DE beginnt
            raise ValueError ("Falscher Anfang")

        if not ust_id [2:].isdigit(): #Nimmt alles ab dem 3. Zeichen 
            raise ValueError("Zahlen fehlen")

        self._ust_id = ust_id

    @property
    def zahlungsziel_tage(self)-> int:
        """Gibt das Zahlugnsziel in Tagen zurück"""
        return self._zahlungsziel_tage

    @zahlungsziel_tage.setter
    def zahlungsziel_tage(self, zahlungsziel_tage: int)-> None:
        """Prüft und speichert ein Zahlungsziel zwischen 0. und 60 Tagen"""

        if zahlungsziel_tage < 0 or zahlungsziel_tage > 60 : # Prüft ob die zahl Kleiner als 0 und größer als 60 ist
            raise ValueError("Eingabe ungültig") # Wenn kleiner als 0 und größer als 60 ist die Eingabe ungültig 

        else:

            self._zahlungsziel_tage = zahlungsziel_tage


    def begruessung(self)->str:
        """gibt eine Begrüßung für den Geschäftskunden zurück"""
        return f"Sehr geehrte Damen und Herren der {self.firmenname},"

    def rabattsatz(self)-> float:
        """Gibt den festen Rabatt von 3% zurück """
        return 0.03

    def __str__(self) ->str:
        """Gibt die Firma und den Ansprechpartner als Text zurück"""
        return f"Kunde {self.kundennummer}: {self.firmenname} (Ansprechpartner: {self.name})"


class Verein(Kunde):
    """ Stellt einen Verein als Kunde dar"""
    def __init__(self, kundennummer: int, name: str, email: str, registernummer: str, gemeinnuetzig: bool = True)-> None:
        """Initialisiert einen Verein mit seinen Angaben"""

        super().__init__(kundennummer, name, email)

        self.registernummer = registernummer
        self.gemeinnuetzig = gemeinnuetzig 


    @property 
    def registernummer(self)-> str:
        """gibt die gespeicherte Registernummer zurück"""
        return self._registernummer

    @registernummer.setter
    def registernummer(self, registernummer: str)-> None: 
        """Prüft und speichert eine gültige Registernummer"""

        if not registernummer.startswith("VR "): #Prüft ob die Registernummer mit VR beginnt
            raise ValueError ("Falscher Anfang")

        if not registernummer[3:].isdigit(): #Nimmt alles ab dem 4. Zeichen 
            raise ValueError("Zahlen fehlen")

        self._registernummer = registernummer 

    def begruessung(self)->str:
            """gibt eine Begrüßung an den Vorstand zurück"""
            return f"An den Vorstand des Vereins {self.name}"
        
    def rabattsatz(self)-> float:
        """Gibt einen Rabatt zurück"""
        
        if self.gemeinnuetzig: # wenn es ein gemeinnütziger Verein ist 
                 

         return 0.05 # wird 5 % Rabbatt gewährt 

        else: # Wenn es kein gemeinnütziger Verein ist 
                

            return 0.02 # wird 2 % Rabatt gewährt
                     


    





    
    




