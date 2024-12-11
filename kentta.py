import mysql.connector
from yhteys import connect_to_db

# KENTTÄ-LUOKKA

class Lentokentta:
    def __init__(self, icao): # Alustaja
        self.icao = icao
        self.connection = connect_to_db()
        if not self.connection:
            raise ConnectionError("Tietokantayhteyttä ei voitu muodostaa.")
        self.cursor = self.connection.cursor()
        self.korkeus = self.hae_korkeus() # kutsutaan aliohjelmaa joka hakee korkeuden
        self.nimi = self.hae_nimi() # kutsutaan aliohjelmaa joka hakee nimen
        self.koordinaatit = self.hae_koordinaatit() # kutsutaan aliohjelmaa joka hakee koordinaatit

    def hae_korkeus(self): # hakee kentän korkeuden SQL tietokannasta

        try:
            query = "SELECT elevation_ft FROM airport WHERE ident = %s"
            self.cursor.execute(query, (self.icao,))
            result = self.cursor.fetchone()
            if result:
                korkeus = result[0] * 0.3048  # Muunna metreiksi
                return korkeus
            else:
                print(f"Lentokentän korkeutta koodilla {self.icao} ei löytynyt.")
                return None
        except mysql.connector.Error as e:
            print(f"Virhe lentokentän korkeuden haussa: {e}")
            return None


    def hae_nimi(self):  # hakee kentän nimen SQL tietokannasta
        try:
            query = "SELECT name FROM airport WHERE ident = %s"
            self.cursor.execute(query, (self.icao,))
            result = self.cursor.fetchone()
            if result:
                nimi = result[0] # asetetan haettu nimi nimeksi
                return nimi
            else:
                print(f"Lentokentän nimeä koodilla {self.icao} ei löytynyt.")
                return None
        except mysql.connector.Error as e:
            print(f"Virhe lentokentän nimen haussa: {e}")
            return None


    def hae_koordinaatit(self):  # hakee kentän koordinaatit SQL tietokannasta
        try:
            query = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s"
            self.cursor.execute(query, (self.icao,))
            result = self.cursor.fetchone()
            if result:
                latitude = result[0]
                longitude = result[1]
                koordinaatit = (latitude, longitude)
                return koordinaatit
            else:
                print(f"Lentokentän koordinaatteja koodilla {self.icao} ei löytynyt.")
                return None
        except mysql.connector.Error as e:
            print(f"Virhe lentokentän koordinaattien haussa: {e}")
            return None

        finally:
            self.close_connection()

    def close_connection(self):
        if self.connection:  # Tarkista, että yhteys on olemassa
            try:
                self.connection.close()
                self.connection = None  # Nollaa yhteys attribuutista
            except mysql.connector.Error as e:
                print(f"Virhe yhteyden sulkemisessa: {e}")
