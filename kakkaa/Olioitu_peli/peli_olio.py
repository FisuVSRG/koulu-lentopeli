import mariadb

# Yhdistäminen tietokantaan
def connect_to_db():
    try:
        connection = mariadb.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='root',
            password='pidätunkkisi',
            autocommit=True
        )
        return connection
    except mariadb.Error as e:
        print(f"Virhe yhteydessä MariaDB:hen: {e}")
        return None

class Peli:

    def __init__(self, game_id):
        """Kutsu antamalla kentta oliosta game_id kutsuessa.
        esim
        kayttaja1 = Kayttaja()
        peli1 = Peli(kayttaja1.game_id)"""

        self.connection = connect_to_db()
        self.cursor = self.connection.cursor()
        self.game_id = game_id

        self.vanhat_yhdistelmat = [] # lista jo käytettyille yhdistelmille

    def vanhat_yhdistelmat(self): # Lisätään yhdistelmä vanhat_yhdistelmät listaan
        if self.connection is None:
            return
        try:
            query = " SELECT airport_ident1, airport_ident2 FROM include WHERE game_id = ?;"
            self.cursor.execute(query, (self.game_id,))
            haetut = self.cursor.fetchall()
            for monikko in haetut:
                self.vanhat_yhdistelmat.append(set(monikko)) # lisätään tuple settinä listaan
        except mariadb.Error as err:
            print(f"Virhe vanhojen yhdistelmien haussa: {err}")


