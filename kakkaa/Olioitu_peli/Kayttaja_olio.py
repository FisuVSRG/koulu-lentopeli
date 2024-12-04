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


class Kayttaja:
    def __init__(self):
        self.connection = connect_to_db()
        if self.connection:  # Yhdistetään tietokantaan olioa luodessa.
            self.cursor = self.connection.cursor()
        self.username = None
        self.user_id = None
        self.game_id = None
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

    def create_game_id(self):
        try:
            query = "INSERT INTO game (user_id) VALUES (?)"
            self.cursor.execute(query, (self.user_id,))
            self.connection.commit()  # Tallennetaan muutokset
            self.game_id = self.cursor.lastrowid
            return self.game_id
        except mariadb.Error as e:
            print(f"Virhe pelin ID:n luomisessa: {e}")
            self.connection.rollback()
            return None

    def tallenna_kayttajatunnus(self):
        if self.connection is None:
            return None, None, None

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

            self.game_id = self.create_game_id()
            if self.game_id is not None:
                return self.game_id, self.username, self.user_id
        except mariadb.Error as e:
            print(f"Virhe käyttäjätunnuksen tallentamisessa: {e}")
        finally:
            self.close_connection()

    def close_connection(self):
        if self.connection:
            self.connection.close()

# testataan
kayttaja1 = Kayttaja()
print(kayttaja1.username)
print(kayttaja1.user_id)
print(kayttaja1.game_id)

