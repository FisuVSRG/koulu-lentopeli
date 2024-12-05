import mariadb
import random
from yhteys import connect_to_db

class Peli:

    def __init__(self, user_id, username, pisteet = 0):
        """Kutsu antamalla kentta oliosta game_id kutsuessa.
        esim
        kayttaja1 = Kayttaja()
        peli1 = Peli(kayttaja1.user_id)"""

        self.connection = connect_to_db()
        if not self.connection:
            raise ConnectionError("Tietokantayhteyttä ei voitu muodostaa.")
        self.cursor = self.connection.cursor()
        self.game_id = self.create_game_id(user_id)
        self.user_id = user_id
        self.username = username
        self.vanhat_yhdistelmat = self.hae_vanhat_yhdistelmat() # lista jo käytettyille yhdistelmille
        self.pisteet = pisteet



    def create_game_id(self, user_id):
        try:
            query = "INSERT INTO game (user_id) VALUES (?)"
            self.cursor.execute(query, (user_id,))
            self.connection.commit()  # Tallennetaan muutokset
            game_id = self.cursor.lastrowid
            self.game_id = game_id
            return self.game_id
        except mariadb.Error as e:
            print(f"Virhe pelin ID:n luomisessa: {e}")
            return None

    def hae_vanhat_yhdistelmat(self):
        """Hakee pelin aiemmat yhdistelmät tietokannasta."""
        vanhat = []
        try:
            query = """
                SELECT airport_ident1, airport_ident2
                FROM include
                WHERE game_id = ?;
            """
            self.cursor.execute(query, (self.game_id,))
            haetut = self.cursor.fetchall()
            for monikko in haetut:
                vanhat.append(set(monikko))
        except mariadb.Error as err:
            print(f"Virhe vanhojen yhdistelmien haussa: {err}")
        return vanhat

    def arvo_kentta(self):
        """Arpoo kaksi lentokenttää ja lisää yhdistelmän tietokantaan."""
        yhdistelma = set()
        try:
            query_count = """
                SELECT COUNT(*) FROM airport
                WHERE type = 'large_airport' AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE');
            """
            self.cursor.execute(query_count)
            kenttien_maara = self.cursor.fetchone()[0]

            while len(yhdistelma) < 2:
                rivi_offset = random.randint(1, kenttien_maara - 1)
                query_random = """
                    SELECT ident FROM airport
                    WHERE type = 'large_airport' AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE')
                    LIMIT 1 OFFSET ?;
                """
                self.cursor.execute(query_random, (rivi_offset,))
                icao = self.cursor.fetchone()[0]
                if icao not in yhdistelma:
                    yhdistelma.add(icao)

                # Varmista, ettei yhdistelmä ole vanhoissa
                if yhdistelma in self.vanhat_yhdistelmat and len(yhdistelma) == 2:
                    yhdistelma.clear()

            # Lisää yhdistelmä tietokantaan
            icao_1, icao_2 = yhdistelma
            query_insert = """
                INSERT INTO include (airport_ident1, airport_ident2, game_id)
                VALUES (?, ?, ?);
            """
            self.cursor.execute(query_insert, (icao_1, icao_2, self.game_id))
            self.connection.commit()
        except mariadb.Error as err:
            print(f"Virhe lentokentän arvonnassa: {err}")
            self.connection.rollback()
        return yhdistelma

    def lisaa_pisteita(self):
        self.pisteet += 100
        return self.pisteet

    def tallenna_pisteet(self):
        """Päivittää pisteitä tietokantaan."""
        try:
            query = "UPDATE game SET score = ? WHERE id = ? AND user_id = ?"
            self.cursor.execute(query, (self.pisteet, self.game_id, self.user_id))
            self.connection.commit()
            print(f"Pisteet tallennettu käyttäjälle: {self.username}, pisteet: {self.pisteet}")
        except mariadb.Error as e:
            print(f"Virhe pisteiden tallentamisessa: {e}")
            self.connection.rollback()

    def close_connection(self):
        if self.connection:  # Tarkista, että yhteys on olemassa
            try:
                self.connection.close()
                self.connection = None  # Nollaa yhteys attribuutista
            except mariadb.Error as e:
                print(f"Virhe yhteyden sulkemisessa: {e}")
