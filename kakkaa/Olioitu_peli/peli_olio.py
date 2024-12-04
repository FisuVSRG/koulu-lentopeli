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

    def __init__(self):
        self.connection = connect_to_db()

        self.game_id = self.create_game_id(user_id) # MISTÄ USER ID TÄHÄN????

        self.vanhat_yhdistelmat = [] # lista jo käytettyille yhdistelmille

    def vanhat_yhdistelmat(self): # Lisätään yhdistelmä vanhat_yhdistelmät listaan
        if self.connection is None:
            return
        try:
            cursor = self.connection.cursor()
            query = " SELECT airport_ident1, airport_ident2 FROM include WHERE game_id = ?;"
            cursor.execute(query, (self.game_id,))
            haetut = cursor.fetchall()
            for monikko in haetut:
                self.vanhat_yhdistelmat.append(set(monikko)) # lisätään tuple settinä listaan
        except mariadb.Error as err:
            print(f"Virhe vanhojen yhdistelmien haussa: {err}")


    def create_game_id(self, user_id):
        if self.connection is None:
            return
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO game (user_id) VALUES (?)"
            cursor.execute(query, (user_id,))
            self.game_id = cursor.lastrowid
            return self.game_id
        except mariadb.Error as e:
            print(f"Virhe pelin ID:n luomisessa: {e}")
            self.connection.rollback()
            return None
        finally:
            if self.connection:
                self.connection.close()