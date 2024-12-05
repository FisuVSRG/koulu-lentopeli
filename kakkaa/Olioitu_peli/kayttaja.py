import mariadb
from yhteys import connect_to_db
# Yhdistäminen tietokantaan



class Kayttaja:
    def __init__(self):
        self.connection = connect_to_db()
        if not self.connection:
            raise ConnectionError("Tietokantayhteyttä ei voitu muodostaa.")
        self.cursor = self.connection.cursor()
        self.username = None
        self.user_id = None
        self.tallenna_kayttajatunnus()

    def check_user_exists(self):
        try:
            query = "SELECT COUNT(*) FROM user WHERE username = ?"
            self.cursor.execute(query, (self.username,))
            result = self.cursor.fetchone()
            return result[0] > 0
        except mariadb.Error as e:
            print(f"Virhe käyttäjän tarkistuksessa: {e}")
            return False

    def add_new_user(self, username):
        try:
            self.username = username
            query = "INSERT INTO user (username) VALUES (?)"
            self.cursor.execute(query, (username,))
            self.connection.commit()  # Tallennetaan muutokset
        except mariadb.Error as e:
            print(f"Virhe uuden käyttäjän lisäämisessä: {e}")
            self.connection.rollback()

    def get_user_id(self):
        try:
            query = "SELECT id FROM user WHERE username = ?"
            self.cursor.execute(query, (self.username,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mariadb.Error as e:
            print(f"Virhe käyttäjän ID:n hakemisessa: {e}")
            return None


    def tallenna_kayttajatunnus(self):
        if self.connection is None:
            return None, None

        try:
            username = input("Anna käyttäjätunnus: ")
            self.username = username  # Aseta käyttäjänimi
            if self.check_user_exists():
                print(f"Tervetuloa takaisin, {self.username}!")
                self.user_id = self.get_user_id()
            else:
                self.add_new_user(username)
                print(f"Tervetuloa peliin, {username}!")
                self.user_id = self.get_user_id()
            return self.username, self.user_id
        except mariadb.Error as e:
            print(f"Virhe käyttäjätunnuksen tallentamisessa: {e}")

    def close_connection(self):
        if self.connection:  # Tarkista, että yhteys on olemassa
            try:
                self.connection.close()
                self.connection = None  # Nollaa yhteys attribuutista
            except mariadb.Error as e:
                print(f"Virhe yhteyden sulkemisessa: {e}")




